"""Command-line interface for lifeline."""

import sys
import click
from pathlib import Path

from lifeline.event import Event
from lifeline.git import add_event_to_git, create_branch, add_past_event
from lifeline.utils import validate_date


@click.group()
def cli():
    """Manage your life timeline using git."""
    pass


@cli.command()
@click.argument('title')
@click.option('--date', required=True, help='Event date in YYYY-MM-DD format.')
@click.option('--type', required=True, help='Type of event (life, education, work, etc).')
@click.option('--description', required=True, help='Brief description of the event.')
@click.option('--media/--no-media', default=False, help='Create a directory for media files.')
def add(title, date, type, description, media):
    """Add a new event to the timeline at the current point."""
    try:
        # Validate date
        validate_date(date)
        
        # Create event
        event = Event(title, date, type, description)
        
        # Save event
        file_path = event.save()
        click.echo(f"Created event file: {file_path}")
        
        # Create media directory if requested
        if media:
            media_dir = event.create_media_dir()
            click.echo(f"Created media directory: {media_dir}")
        
        # Add to git
        add_event_to_git(file_path, date, title)
        click.echo(f"Added event to git: {title} on {date}")
        
    except Exception as e:
        click.echo(f"Error: {e}", err=True)
        sys.exit(1)


@cli.group()
def branch():
    """Manage alternate timeline branches."""
    pass


@branch.command('create')
@click.argument('name')
@click.option('--commit', help='Commit hash to branch from (default: HEAD).')
def branch_create(name, commit):
    """Create a new branch representing an alternate timeline."""
    try:
        create_branch(name, commit)
        click.echo(f"Created branch: {name}")
    except Exception as e:
        click.echo(f"Error: {e}", err=True)
        sys.exit(1)


@cli.command()
@click.argument('title')
@click.option('--date', required=True, help='Event date in YYYY-MM-DD format.')
@click.option('--type', required=True, help='Type of event (life, education, work, etc).')
@click.option('--description', required=True, help='Brief description of the event.')
@click.option('--base', help='Commit hash to insert after (default: earliest commit).')
@click.option('--media/--no-media', default=False, help='Create a directory for media files.')
def add_past(title, date, type, description, base, media):
    """Add an event to the timeline at a past point."""
    try:
        # Validate date
        validate_date(date)
        
        # Create event
        event = Event(title, date, type, description)
        
        # Save event
        file_path = event.save()
        click.echo(f"Created event file: {file_path}")
        
        # Create media directory if requested
        if media:
            media_dir = event.create_media_dir()
            click.echo(f"Created media directory: {media_dir}")
        
        # Add to git at a past point
        add_past_event(file_path, date, title, base)
        click.echo(f"Added past event to git: {title} on {date}")
        
    except Exception as e:
        click.echo(f"Error: {e}", err=True)
        sys.exit(1)


if __name__ == '__main__':
    cli() 