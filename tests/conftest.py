import os
import shutil
import pytest
from pathlib import Path
from git import Repo

@pytest.fixture
def temp_repo(tmp_path):
    """Create a temporary git repository for testing."""
    repo_path = tmp_path / "test_repo"
    repo_path.mkdir()
    
    # Initialize git repo
    repo = Repo.init(repo_path)
    
    # Create events directory
    events_dir = repo_path / "events"
    events_dir.mkdir()
    
    # Set up git config
    with repo.config_writer() as git_config:
        git_config.set_value('user', 'name', 'Test User')
        git_config.set_value('user', 'email', 'test@example.com')
    
    yield repo_path
    
    # Cleanup
    shutil.rmtree(repo_path)

@pytest.fixture
def repo_with_events(temp_repo):
    """Create a temporary git repository with some sample events."""
    events_dir = temp_repo / "events"
    
    # Create some sample events
    event1_path = events_dir / "2023-01-01_test-event-1.md"
    event1_path.write_text("# Test Event 1\nThis is a test event.")
    
    event2_path = events_dir / "2023-02-01_test-event-2.md"
    event2_path.write_text("# Test Event 2\nThis is another test event.")
    
    repo = Repo(temp_repo)
    repo.index.add([str(event1_path), str(event2_path)])
    repo.index.commit("Initial test events")
    
    return temp_repo 