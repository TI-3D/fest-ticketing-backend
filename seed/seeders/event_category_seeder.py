from app.models import EventCategories
from sqlalchemy.orm import Session

def create_event_categories(session: Session):
    list_event_categories = [
        "Music & Concerts", 
        "Food & Drink Festivals", 
        "Business & Entrepreneurship", 
        "Health & Wellness", 
        "Science & Technology", 
        "Travel & Adventure", 
        "Charity & Social Causes", 
        "Community & Networking", 
        "Family & Educational Events", 
        "Fashion & Style", 
        "Film, Media & Entertainment", 
        "Government & Politics", 
        "Hobbies & Craftsmanship", 
        "Holiday & Seasonal Celebrations", 
        "Home, Lifestyle & Design", 
        "Performing & Visual Arts", 
        "School & Academic Activities", 
        "Spiritual & Religious Gatherings", 
        "Sports & Fitness Competitions", 
        "Automotive, Boat & Air Shows"
    ]

    
    for category_name in list_event_categories:
        event_category = EventCategories(
            category_name=category_name
        )
        session.add(event_category)
    
    session.commit()
    print(f"Generated {len(list_event_categories)} event categories.")
    
def delete_all_event_categories(session: Session):
    session.query(EventCategories).delete()
    session.commit()
    print("Deleted all event categories.")
