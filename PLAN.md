# Life Timeline: Git-Based Event Management System

## Overview

This system will use git as a backend for managing life events on a timeline. Events will be stored as markdown files (and potentially other media) in an "events" folder. The system will leverage git's version control features to manage the chronology of events, with each commit representing a single event at a specific point in time.

## Core Concepts

1. **Events as Files**: Each event is stored as a markdown file (and potentially associated media files) in the "events" folder, with date-based naming.
2. **Commits as Timeline Points**: Each commit represents a single event at a specific point in time.
3. **Branches as Alternate Timelines**: Git branches can represent alternate timelines or possible futures.
4. **Rebasing for Historical Edits**: Adding events in the past involves rebasing the timeline.
5. **Linear History**: The main branch maintains a linear history of events.

## System Architecture

### Directory Structure
```
life-timeline/
├── index.html              # Frontend visualization
├── events/                 # Directory containing all events
│   ├── 2023-12-25_event1.md  # Date-prefixed markdown file
│   ├── 2023-12-25_event1/    # Optional folder for event media
│   │   ├── photo1.jpg
│   │   └── video1.mp4
│   └── ...
├── lifeline/              # Python package directory
│   ├── __init__.py       # Package initialization
│   ├── cli.py            # CLI command definitions
│   ├── event.py          # Event class and operations
│   ├── git.py            # Git operations wrapper
│   ├── parser.py         # Timeline parsing
│   ├── utils.py          # Shared utilities
│   └── event.md.j2       # Event template
├── pyproject.toml        # Project metadata and dependencies
└── README.md            # Documentation
```

### Event Files Format and Naming

Events follow a standardized naming convention and format:

**File naming:**
```
YYYY-MM-DD_slugified-event-title.md
```

**Content format:**
```markdown
---
title: Event Title
date: YYYY-MM-DD
type: life|education|work|etc
description: Brief description of the event
---

Detailed markdown content about the event...

![Image description](./YYYY-MM-DD_slugified-event-title/image.jpg)
```

## Implementation Tasks

1. **Setup Basic Repository Structure**
   - Initialize git repository
   - Create package structure
   - Create pyproject.toml with dependencies
   - Update README with system documentation

2. **Develop Core Package**
   - `lifeline/utils.py`: Shared utilities
     - Date validation and formatting
     - Slugify title for filenames
     - File operations
     - Configuration management

   - `lifeline/event.py`: Event management
     - Event class with properties
     - Event file creation and parsing
     - Event validation
     - Event template rendering

   - `lifeline/git.py`: Git operations
     - Repository management
     - Commit operations
     - Branch and rebase utilities

   - `lifeline/parser.py`: Timeline parsing
     - Git history parsing
     - Event data extraction
     - JSON generation for visualization

   - `lifeline/cli.py`: Command-line interface
     - Command group setup
     - Event commands (add, add-past)
     - Branch commands
     - Parse command

3. **Implement CLI Commands**
   ```python
   # In lifeline/cli.py
   @click.group()
   def cli():
       """Manage your life timeline using git."""
       pass

   @cli.command()
   @click.argument('title')
   @click.option('--date', required=True)
   @click.option('--type', required=True)
   @click.option('--description', required=True)
   def add(title, date, type, description):
       """Add a new event to the timeline."""
       pass

   @cli.command()
   def parse():
       """Generate timeline visualization data."""
       pass
   ```

4. **Update Frontend Visualization**
   - Modify index.html to fetch data from parser output
   - Enhance visualization to display branches
   - Add UI elements for timeline management

5. **Testing and Validation**
   - Unit tests for core functionality
   - Integration tests for git operations
   - CLI tests
   - Date-based sorting validation

6. **Documentation**
   - API documentation
   - CLI usage documentation
   - Git concepts explanation

## CLI Operations

### Adding a New Event
```bash
# Create event file
lifeline add "New Year Party" --date "2023-12-25" --type "life" --description "Celebrated New Year"

# Under the hood, this:
# 1. Creates 2023-12-25_new-year-party.md
# 2. git add events/2023-12-25_new-year-party.md
# 3. git commit -m "Add event: New Year Party" --date="2023-12-25"
```

### Creating an Alternate Timeline
```bash
# Create branch from a specific commit
lifeline branch create "alternate-future" --commit <hash>

# Under the hood, this:
# git checkout -b alternate-future <commit-hash>
```

### Adding an Event in the Past
```bash
# Add event at a specific point in the past
lifeline add-past "College Start" --date "2020-01-15" --type "education" --description "Started college" --base <hash>

# Under the hood, this:
# 1. Creates temporary branch
# 2. Creates 2020-01-15_college-start.md
# 3. Adds and commits the event
# 4. Rebases the timeline
# 5. Merges back to main with linear history
```

### Parsing Timeline
```bash
# Generate timeline data for visualization
lifeline parse > timeline_data.json
```

## Dependencies

Project dependencies in pyproject.toml:
```toml
[project]
name = "lifeline"
version = "0.1.0"
description = "Git-based life timeline management system"
dependencies = [
    "gitpython>=3.1.0",
    "python-slugify>=8.0.0",
    "pyyaml>=6.0.0",
    "click>=8.0.0",
    "jinja2>=3.0.0",
]

[project.scripts]
lifeline = "lifeline.cli:cli"
```

## Next Steps

After implementing the basic system, we can consider additional features:
- Web interface for managing events without command line
- Automatic visualization updates when new events are added
- Support for more media types (audio, documents, etc.)
- Integration with backup systems
- Multi-user collaboration features
- Privacy controls for sensitive events 