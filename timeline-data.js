// Define timeline data as a global variable
const TIMELINE_DATA = {
    "nodes": [
        { "id": "birth", "name": "Birth", "date": "1990-01-01", "description": "The beginning of your journey.", "type": "milestone" },
        { "id": "today", "name": "Today", "date": "2023-06-05", "description": "Your current position in the timeline.", "type": "present" },
        { "id": "school", "name": "Started School", "date": "1995-09-01", "description": "First day of elementary school.", "type": "education" },
        { "id": "highschool", "name": "High School", "date": "2004-09-01", "description": "Started high school.", "type": "education" },
        { "id": "college", "name": "College", "date": "2008-09-01", "description": "Started college education.", "type": "education" },
        { "id": "graduation", "name": "Graduation", "date": "2012-05-15", "description": "Graduated from college with a degree.", "type": "milestone" },
        { "id": "firstjob", "name": "First Job", "date": "2012-07-10", "description": "Started first professional job.", "type": "career" },
        { "id": "moved", "name": "Moved to New City", "date": "2015-03-20", "description": "Relocated to a new city for better opportunities.", "type": "life" },
        { "id": "promotion", "name": "Major Promotion", "date": "2018-11-05", "description": "Received a significant promotion at work.", "type": "career" },
        { "id": "travel", "name": "World Travel", "date": "2024-06-01", "description": "Plan to travel around the world for 3 months.", "type": "goal" },
        { "id": "house", "name": "Buy a House", "date": "2025-01-15", "description": "Goal to purchase first home.", "type": "goal" },
        { "id": "business", "name": "Start Business", "date": "2026-03-10", "description": "Launch own business venture.", "type": "goal" },
        { "id": "family", "name": "Start Family", "date": "2027-05-20", "description": "Begin a family.", "type": "goal" },
        { "id": "retirement", "name": "Early Retirement", "date": "2040-01-01", "description": "Goal to achieve financial independence and retire early.", "type": "goal" },
        { "id": "coolthings", "name": "say hi", "date": "2028-01-01", "description": "doing cool stuff", "type": "cool thing" }

    ],
    "links": [
        { "source": "birth", "target": "school" },
        { "source": "school", "target": "highschool" },
        { "source": "highschool", "target": "college" },
        { "source": "college", "target": "graduation" },
        { "source": "graduation", "target": "firstjob" },
        { "source": "firstjob", "target": "moved" },
        { "source": "moved", "target": "promotion" },
        { "source": "promotion", "target": "today" },
        { "source": "today", "target": "travel" },
        { "source": "today", "target": "house" },
        { "source": "house", "target": "business" },
        { "source": "house", "target": "family" },
        { "source": "business", "target": "retirement" },
        { "source": "family", "target": "retirement" }
    ]
}; 