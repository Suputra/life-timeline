#!/usr/bin/env python3

import os
import sys
import argparse
import datetime
import subprocess
from pathlib import Path
import shutil
import re
from typing import Optional, List, Tuple

class GitError(Exception):
    """Custom exception for git operations."""
    pass

class EventManager:
    def __init__(self):
        self.events_dir = Path('events')
        self.media_dir = Path('media')
        
        # Ensure directories exist
        self.events_dir.mkdir(exist_ok=True)
        self.media_dir.mkdir(exist_ok=True)

    def run_git_command(self, args: List[str], check: bool = True) -> Tuple[int, str, str]:
        """Run a git command and return its output."""
        try:
            print(f"Running git command: git {' '.join(args)}")  # Debug output
            process = subprocess.run(['git'] + args, 
                                  capture_output=True, 
                                  text=True)
            print(f"Return code: {process.returncode}")  # Debug output
            print(f"Stdout: {process.stdout.strip()}")  # Debug output
            print(f"Stderr: {process.stderr.strip()}")  # Debug output
            
            if check and process.returncode != 0:
                raise GitError(f"Git command failed: {process.stderr.strip()}")
            return process.returncode, process.stdout.strip(), process.stderr.strip()
        except subprocess.CalledProcessError as e:
            raise GitError(f"Git command failed: {e}")

    def ensure_git_config(self):
        """Ensure git is configured with user information."""
        try:
            print("Checking git configuration...")  # Debug output
            self.run_git_command(['config', 'user.name'], check=False)
            self.run_git_command(['config', 'user.email'], check=False)
        except GitError:
            print("Configuring git user information...")
            self.run_git_command(['config', 'user.name', 'Life Timeline'])
            self.run_git_command(['config', 'user.email', 'timeline@example.com'])

    def get_current_branch(self) -> str:
        """Get the name of the current git branch."""
        _, output, _ = self.run_git_command(['branch', '--show-current'])
        return output.strip() or 'main'  # Default to 'main' if no branch exists

    def create_branch(self, branch_name: str):
        """Create and switch to a new git branch."""
        self.run_git_command(['checkout', '-b', branch_name])
        print(f"Created and switched to new branch: {branch_name}")

    def get_commit_dates(self) -> List[Tuple[str, datetime.datetime]]:
        """Get all commit dates in chronological order."""
        try:
            _, output, _ = self.run_git_command(
                ['log', '--format=%H %aI', '--reverse'],
                check=False
            )
            commits = []
            for line in output.splitlines():
                if line:
                    commit_hash, date_str = line.split(' ', 1)
                    date = datetime.datetime.fromisoformat(date_str.strip())
                    commits.append((commit_hash, date))
            return commits
        except GitError:
            return []  # Return empty list if no commits exist

    def find_insertion_point(self, target_date: datetime.datetime) -> Optional[str]:
        """Find the appropriate commit for rebasing a past event."""
        commits = self.get_commit_dates()
        if not commits:
            return None
        
        # Find the first commit that comes after our target date
        for commit_hash, date in commits:
            if date > target_date:
                return commit_hash
        
        return None

    def sanitize_filename(self, title: str) -> str:
        """Convert a title to a filename-safe slug."""
        slug = title.lower().replace(' ', '-')
        slug = re.sub(r'[^a-z0-9-]', '', slug)
        slug = re.sub(r'-+', '-', slug)
        return slug

    def create_event(self, date_str: str, title: str, event_type: str, 
                    description: str, media_files: Optional[List[str]] = None,
                    branch_name: Optional[str] = None) -> bool:
        """Create a new event with the given parameters."""
        try:
            # Ensure git is configured
            self.ensure_git_config()
            
            # Validate and parse date
            date = datetime.datetime.strptime(date_str, '%Y-%m-%d')
            date_str = date.strftime('%Y-%m-%d')
            
            # Create new branch if specified
            if branch_name:
                self.create_branch(branch_name)
            
            # Create filename from date and title
            slug = self.sanitize_filename(title)
            event_filename = f"{date_str}-{slug}.md"
            event_path = self.events_dir / event_filename

            print(f"Creating event file: {event_path}")  # Debug output

            # Create media directory if media files are provided
            media_dir = None
            if media_files:
                media_dir = self.media_dir / f"{date_str}-{slug}"
                media_dir.mkdir(parents=True, exist_ok=True)

            # Create event markdown file
            with open(event_path, 'w') as f:
                f.write('---\n')
                f.write(f'title: {title}\n')
                f.write(f'type: {event_type}\n')
                f.write(f'date: {date_str}\n')
                f.write(f'description: {description}\n')
                
                if media_files:
                    f.write('media:\n')
                    for media_file in media_files:
                        target_path = media_dir / Path(media_file).name
                        f.write(f'  - {target_path.relative_to(Path())}\n')
                
                f.write('---\n\n')
                f.write(f'# {title}\n\n')
                f.write(f'{description}\n\n')

                # Add media file references if any
                if media_files:
                    for media_file in media_files:
                        filename = Path(media_file).name
                        target_path = media_dir / filename
                        ext = Path(filename).suffix.lower()
                        if ext in ['.jpg', '.jpeg', '.png', '.gif']:
                            f.write(f'![{filename}](../{target_path.relative_to(Path())})\n')
                        else:
                            f.write(f'[{filename}](../{target_path.relative_to(Path())})\n')

            # Copy media files if provided
            if media_files:
                for media_file in media_files:
                    source = Path(media_file)
                    if not source.exists():
                        print(f"Warning: Media file {media_file} not found")
                        continue
                    target = media_dir / source.name
                    shutil.copy2(source, target)

            print("Staging changes...")  # Debug output
            # Stage the changes
            self.run_git_command(['add', str(event_path)])
            if media_files:
                self.run_git_command(['add', str(media_dir)])

            print("Committing changes...")  # Debug output
            # Commit the event
            commit_msg = f'event: {title} ({date_str})'
            self.run_git_command(['commit', '-m', f'"{commit_msg}"'])
            print(f"Created and committed event: {event_path}")

            # Handle past events by rebasing if necessary
            current_date = datetime.datetime.now().replace(tzinfo=None)
            if date < current_date and not branch_name:
                insertion_point = self.find_insertion_point(date)
                if insertion_point:
                    print(f"This is a past event. Rebasing to maintain chronological order...")
                    try:
                        self.run_git_command(['rebase', '-i', f'{insertion_point}^'])
                        print("Rebase successful!")
                    except GitError as e:
                        print(f"Rebase failed: {e}")
                        print("Please resolve conflicts manually and run 'git rebase --continue'")
                        return False

            return True

        except (ValueError, GitError) as e:
            print(f"Error: {str(e)}")
            return False

    def list_events(self):
        """List all events in chronological order."""
        events = []
        
        for event_file in self.events_dir.glob('*.md'):
            with open(event_file) as f:
                content = f.read()
                date_match = re.search(r'date: (\d{4}-\d{2}-\d{2})', content)
                title_match = re.search(r'title: (.+)', content)
                type_match = re.search(r'type: (.+)', content)
                
                if date_match and title_match and type_match:
                    events.append({
                        'date': date_match.group(1),
                        'title': title_match.group(1),
                        'type': type_match.group(1),
                        'file': event_file.name
                    })
        
        # Sort events by date
        events.sort(key=lambda x: x['date'])
        
        # Print events
        current_branch = self.get_current_branch()
        print(f"\nEvents on branch: {current_branch}\n")
        
        for event in events:
            print(f"{event['date']} - [{event['type']}] {event['title']}")

    def list_branches(self):
        """List all timeline branches."""
        _, output, _ = self.run_git_command(['branch'])
        print("\nTimeline branches:")
        for branch in output.splitlines():
            print(branch)

def main():
    manager = EventManager()
    parser = argparse.ArgumentParser(description='Manage life timeline events')
    subparsers = parser.add_subparsers(dest='command', help='Commands')

    # Create event command
    create_parser = subparsers.add_parser('create', help='Create a new event')
    create_parser.add_argument('--date', required=True, help='Event date (YYYY-MM-DD)')
    create_parser.add_argument('--title', required=True, help='Event title')
    create_parser.add_argument('--type', required=True, help='Event type (life/education/work/etc)')
    create_parser.add_argument('--description', required=True, help='Event description')
    create_parser.add_argument('--media', nargs='*', help='Media files to include')
    create_parser.add_argument('--branch', help='Create event in a new branch (for alternate timelines)')

    # List events command
    list_parser = subparsers.add_parser('list', help='List all events')

    # List branches command
    branches_parser = subparsers.add_parser('branches', help='List all timeline branches')

    args = parser.parse_args()

    try:
        if args.command == 'create':
            manager.create_event(args.date, args.title, args.type, args.description, args.media, args.branch)
        elif args.command == 'list':
            manager.list_events()
        elif args.command == 'branches':
            manager.list_branches()
        else:
            parser.print_help()
    except GitError as e:
        print(f"Git error: {str(e)}")
        sys.exit(1)
    except Exception as e:
        print(f"Error: {str(e)}")
        sys.exit(1)

if __name__ == '__main__':
    main() 