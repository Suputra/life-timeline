def is_repo_clean(repo_path='.'):
    """
    Check if the git repository is clean (no uncommitted changes or untracked files).
    
    Args:
        repo_path: Path to the repository (default: current directory)
    
    Returns:
        bool: True if clean, False otherwise
    """
    repo = get_repo(repo_path)
    return not (repo.is_dirty() or repo.untracked_files)

def add_event_to_git(file_path, event_date=None, title=None, repo_path=None):
    """
    Add an event file to git and commit it.
    
    Args:
        file_path: Path to the event file
        event_date: Date of the event (for commit date)
        title: Title of the event (for commit message)
        repo_path: Path to the repository (default: directory containing file_path)
        
    Returns:
        git.Commit object
    """
    # If repo_path not provided, use the directory containing the file
    if repo_path is None:
        repo_path = str(Path(file_path).parent.parent)
    
    repo = get_repo(repo_path)
    
    # Convert file_path to be relative to repo root if it's absolute
    abs_file_path = str(Path(file_path).absolute())
    repo_root = str(Path(repo.working_dir).absolute())
    if abs_file_path.startswith(repo_root):
        file_path = str(Path(abs_file_path).relative_to(repo_root))
    
    # Add the file to git
    repo.index.add([file_path])
    
    # Create commit message
    commit_msg = f"Add event: {title}" if title else f"Add event from {Path(file_path).name}"
    
    # Commit with the event date if provided
    if event_date:
        # Convert to git-compatible date format
        git_date = datetime.strptime(event_date, "%Y-%m-%d").strftime("%Y-%m-%d %H:%M:%S")
        return repo.index.commit(commit_msg, author_date=git_date, commit_date=git_date)
    else:
        return repo.index.commit(commit_msg) 