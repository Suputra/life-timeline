# Life Timeline

A Git-based life timeline management system that uses git's version control features to manage a chronological history of life events.

## Features

- Store life events as markdown files with associated media
- Use git commits to represent the chronology of events
- Create alternate timelines/possible futures using branches
- Add events in the past using git rebase
- Visualize your timeline in the browser

## Installation

Clone the repository and install:

```bash
git clone https://github.com/yourusername/life-timeline.git
cd life-timeline
pip install -e .
```

## Usage

### Adding a new event

```bash
lifeline add "Started New Job" --date "2023-01-15" --type "work" --description "Began working at Company XYZ" --media
```

### Creating an alternate timeline

```bash
lifeline branch create "alternate-career"
```

### Adding an event in the past

```bash
lifeline add-past "College Graduation" --date "2019-05-20" --type "education" --description "Graduated with honors" --media
```

## Event Types

The system recognizes the following event types:
- life (general life events)
- education (school, college, courses)
- work (jobs, promotions)
- travel (trips, vacations)
- health (medical events)

## Directory Structure

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
└── ...
```

## Event File Format

Events are stored as markdown files with YAML frontmatter:

```markdown
---
title: Event Title
date: YYYY-MM-DD
type: life|education|work|travel|health
description: Brief description of the event
---

Detailed markdown content about the event...

![Image description](./YYYY-MM-DD_slugified-event-title/image.jpg)
```

## License

MIT 