"""Utility functions for the lifeline package."""

import os
import re
from datetime import datetime
from pathlib import Path
from slugify import slugify

# Constants
EVENTS_DIR = "events"
DEFAULT_EVENT_TYPES = ["life", "education", "work", "travel", "health"]


def validate_date(date_str):
    """
    Validate that a date string is in YYYY-MM-DD format.
    
    Args:
        date_str: Date string to validate
        
    Returns:
        datetime object if valid
        
    Raises:
        ValueError: If date format is invalid
    """
    try:
        return datetime.strptime(date_str, "%Y-%m-%d")
    except ValueError:
        raise ValueError(
            f"Invalid date format: {date_str}. Expected format: YYYY-MM-DD"
        )


def validate_event_type(event_type, allowed_types=None):
    """
    Validate that an event type is allowed.
    
    Args:
        event_type: Event type to validate
        allowed_types: List of allowed types (defaults to DEFAULT_EVENT_TYPES)
        
    Returns:
        event_type if valid
        
    Raises:
        ValueError: If event type is not allowed
    """
    if allowed_types is None:
        allowed_types = DEFAULT_EVENT_TYPES
    
    if event_type not in allowed_types:
        raise ValueError(
            f"Invalid event type: {event_type}. Allowed types: {', '.join(allowed_types)}"
        )
    
    return event_type


def get_event_filename(date_str, title):
    """
    Generate a filename for an event.
    
    Args:
        date_str: Date string in YYYY-MM-DD format
        title: Event title
        
    Returns:
        Filename in format: YYYY-MM-DD_slugified-title.md
    """
    # Validate date format
    validate_date(date_str)
    
    # Slugify the title
    slug = slugify(title)
    
    return f"{date_str}_{slug}.md"


def ensure_events_dir():
    """
    Ensure that the events directory exists.
    
    Returns:
        Path to the events directory
    """
    events_path = Path(EVENTS_DIR)
    events_path.mkdir(exist_ok=True)
    return events_path 