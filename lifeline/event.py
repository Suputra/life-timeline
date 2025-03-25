"""Event management for lifeline."""

import os
from pathlib import Path
import yaml
from jinja2 import Template

from lifeline.utils import (
    validate_date,
    validate_event_type,
    get_event_filename,
    ensure_events_dir,
    EVENTS_DIR
)


class Event:
    """Class representing a timeline event."""
    
    def __init__(self, title, date, event_type, description):
        """
        Initialize a new event.
        
        Args:
            title: Event title
            date: Event date in YYYY-MM-DD format
            event_type: Type of event
            description: Brief description of the event
        """
        self.title = title
        self.date = validate_date(date)
        self.date_str = date  # Keep original string format
        self.event_type = validate_event_type(event_type)
        self.description = description
        self.filename = get_event_filename(date, title)
    
    @property
    def path(self):
        """Get the path to the event file."""
        return os.path.join(EVENTS_DIR, self.filename)
    
    @property
    def media_dir(self):
        """Get the path to the event media directory."""
        return os.path.join(EVENTS_DIR, self.filename.replace('.md', ''))
    
    @classmethod
    def from_file(cls, file_path):
        """
        Create an Event from an existing markdown file.
        
        Args:
            file_path: Path to the markdown file
            
        Returns:
            Event object
        """
        # Read the file
        with open(file_path, 'r') as f:
            content = f.read()
        
        # Split content and frontmatter
        parts = content.split('---', 2)
        if len(parts) < 3:
            raise ValueError(f"Invalid event file format: {file_path}")
        
        # Parse frontmatter
        frontmatter = yaml.safe_load(parts[1])
        
        # Create event
        return cls(
            frontmatter['title'],
            frontmatter['date'],
            frontmatter['type'],
            frontmatter['description']
        )
    
    def to_markdown(self):
        """
        Convert the event to markdown format.
        
        Returns:
            Markdown string
        """
        # Read the template
        template_path = Path(__file__).parent / 'event.md.j2'
        with open(template_path, 'r') as f:
            template_content = f.read()
        
        # Render the template
        template = Template(template_content)
        return template.render(
            title=self.title,
            date=self.date_str,
            type=self.event_type,
            description=self.description
        )
    
    def save(self):
        """
        Save the event to a file.
        
        Returns:
            Path to the created file
        """
        # Ensure events directory exists
        ensure_events_dir()
        
        # Write the file
        file_path = self.path
        with open(file_path, 'w') as f:
            f.write(self.to_markdown())
        
        return file_path
    
    def create_media_dir(self):
        """
        Create a directory for media files.
        
        Returns:
            Path to the created directory
        """
        media_path = Path(self.media_dir)
        media_path.mkdir(exist_ok=True)
        return media_path 