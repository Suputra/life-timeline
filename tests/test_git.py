import os
import shutil
import tempfile
from pathlib import Path
from datetime import datetime
import pytest
import git
from lifeline.git import (
    get_repo,
    is_repo_clean,
    add_event_to_git,
    create_branch,
    checkout_branch,
    add_past_event
)

@pytest.fixture
def temp_repo():
    """Create a temporary repository for testing."""
    temp_dir = tempfile.mkdtemp()
    old_cwd = os.getcwd()
    os.chdir(temp_dir)
    
    # Initialize repo
    repo = git.Repo.init(temp_dir)
    
    # Create initial commit so we have a base
    Path("README.md").write_text("Test Repository")
    repo.index.add(["README.md"])
    repo.index.commit("Initial commit")
    
    yield temp_dir
    
    # Cleanup
    os.chdir(old_cwd)
    shutil.rmtree(temp_dir)

def test_get_repo(temp_repo):
    """Test getting repository object."""
    repo = get_repo(temp_repo)
    assert isinstance(repo, git.Repo)
    assert not repo.bare

def test_is_repo_clean(temp_repo):
    """Test checking if repository is clean."""
    assert is_repo_clean(temp_repo)
    
    # Make a change
    Path("test.txt").write_text("test")
    assert not is_repo_clean(temp_repo)

def test_add_event_to_git(temp_repo):
    """Test adding an event to git."""
    # Create events directory
    events_dir = Path(temp_repo) / "events"
    events_dir.mkdir()
    
    # Create test event
    event_path = events_dir / "2024-01-01_test-event.md"
    event_path.write_text("Test event content")
    
    # Add event
    add_event_to_git(
        str(event_path),
        event_date="2024-01-01",
        title="Test Event",
        repo_path=temp_repo
    )
    
    # Verify commit
    repo = get_repo(temp_repo)
    latest_commit = next(repo.iter_commits())
    assert "Add event: Test Event" in latest_commit.message
    assert "events/2024-01-01_test-event.md" in latest_commit.stats.files

def test_create_and_checkout_branch(temp_repo):
    """Test branch creation and checkout."""
    branch_name = "test-branch"
    
    # Create branch
    create_branch(branch_name, repo_path=temp_repo)
    
    # Verify branch exists and is checked out
    repo = get_repo(temp_repo)
    assert branch_name in [h.name for h in repo.heads]
    assert repo.active_branch.name == branch_name
    
    # Switch back to main
    checkout_branch("main", repo_path=temp_repo)
    assert repo.active_branch.name == "main"

def test_add_past_event(temp_repo):
    """Test adding an event in the past."""
    events_dir = Path(temp_repo) / "events"
    events_dir.mkdir()
    
    # Create some events with different dates
    events = [
        ("2024-03-01", "Future Event"),
        ("2024-01-01", "Past Event"),
    ]
    
    for date, title in events:
        event_path = events_dir / f"{date}_test-event.md"
        event_path.write_text(f"{title} content")
        add_event_to_git(
            str(event_path),
            event_date=date,
            title=title,
            repo_path=temp_repo
        )
    
    # Add an event in between
    middle_event_path = events_dir / "2024-02-01_middle-event.md"
    middle_event_path.write_text("Middle event content")
    
    add_past_event(
        str(middle_event_path),
        event_date="2024-02-01",
        title="Middle Event",
        repo_path=temp_repo
    )
    
    # Verify chronological order
    repo = get_repo(temp_repo)
    commits = list(repo.iter_commits(reverse=True))
    dates = []
    
    for commit in commits:
        if "Add event:" in commit.message:
            commit_date = datetime.fromtimestamp(commit.committed_date)
            dates.append(commit_date)
    
    # Check that dates are in chronological order
    assert all(dates[i] <= dates[i+1] for i in range(len(dates)-1)) 