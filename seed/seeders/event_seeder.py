import os
import random
from datetime import timedelta, datetime
from sqlalchemy.orm import Session
from sqlalchemy.sql import select
from faker import Faker
from app.models import (
    Event, EventCategories, EventOrganizer, EventClass, EventStatus,
    EventCategoryAssociation, Schedule, DayOfWeek, Province, City, District, Village, EventImage
)
from app.services.cloudinary_service import CloudinaryService

fake = Faker()

def fetch_related_data(session: Session):
    """
    Fetch event categories, organizers, and provinces from the database.
    """
    event_categories = session.execute(select(EventCategories)).scalars().all()
    organizers = session.execute(select(EventOrganizer)).scalars().all()
    provinces = session.execute(select(Province)).scalars().all()
    return event_categories, organizers, provinces

def fetch_location_data(session: Session, selected_province):
    """
    Fetch city, district, and village for a given province.
    """
    selected_city = random.choice(
        session.execute(select(City).where(City.code_province == selected_province.code_province)).scalars().all()
    )
    selected_district = random.choice(
        session.execute(select(District).where(District.code_city == selected_city.code_city)).scalars().all()
    )
    selected_village = random.choice(
        session.execute(select(Village).where(Village.code_district == selected_district.code_district)).scalars().all()
    )
    return selected_city, selected_district, selected_village

def upload_event_images(cloudinary_service, image_root_dir, folder_name):
    """
    Upload images from the event image directory to Cloudinary.
    """
    folder_path = os.path.join(image_root_dir, folder_name)
    image_urls = []
    
    if os.path.isdir(folder_path):
        for image_file in os.listdir(folder_path):
            if image_file.lower().endswith(('.jpg', '.jpeg', '.png')):
                image_path = os.path.join(folder_path, image_file)
                image_url = cloudinary_service.upload_image(image_path, folder_name='events')
                if image_url:
                    image_urls.append(image_url['secure_url'])
    return image_urls

def create_event(session: Session, cloudinary_service, event_categories, organizers, provinces, image_root_dir):
    """
    Create a single event with its associated classes, schedules, categories, and images.
    """
    selected_organizer = random.choice(organizers)
    selected_province = random.choice(provinces)
    selected_city, selected_district, selected_village = fetch_location_data(session, selected_province)
    selected_categories = random.sample(event_categories, random.randint(1, 3))

    # Create the event
    event = Event(
        name=fake.sentence(nb_words=4),
        description=fake.text(max_nb_chars=200),
        location=fake.address(),
        status=random.choice(list(EventStatus)),
        organizer_id=selected_organizer.organizer_id,
        code_province=selected_province.code_province,
        code_city=selected_city.code_city,
        code_district=selected_district.code_district,
        code_village=selected_village.code_village,
    )
    session.add(event)
    session.commit()  # Commit to generate `event_id`

    # Add event classes (VIP, Regular, Student)
    for class_name, base_price, description in [
        ("VIP", 1000000, "VIP class"),
        ("Regular", 500000, "Regular class"),
        ("Student", 300000, "Student class"),
    ]:
        event_class = EventClass(
            event_id=event.event_id,
            class_name=class_name,
            base_price=base_price,
            description=description,
            count=random.randint(5, 50),  # Random number of classes
        )
        session.add(event_class)

    # Add schedules
    for _ in range(random.randint(1, 3)):  # Random number of schedules
        start_time = fake.time_object()
        start_datetime = datetime.combine(datetime.today(), start_time)
        end_datetime = start_datetime + timedelta(hours=random.randint(1, 3))  # Random duration of 1-3 hours
        schedule = Schedule(
            event_id=event.event_id,
            day_of_week=random.choice(list(DayOfWeek)),
            date=fake.date_between(start_date="today", end_date="+30d"),
            start_time=start_datetime,
            end_time=end_datetime,
        )
        session.add(schedule)

    # Link event to selected categories
    for category in selected_categories:
        event_category_association = EventCategoryAssociation(
            event_id=event.event_id,
            category_name=category.category_name,
        )
        session.add(event_category_association)

    # Upload and link images
    folder_name = random.choice(os.listdir(image_root_dir))  # Randomly choose a folder
    image_urls = upload_event_images(cloudinary_service, image_root_dir, folder_name)
    
    for image_url in image_urls:
        event_image = EventImage(
            event_id=event.event_id,
            image_url=image_url,
        )
        session.add(event_image)

    session.commit()

def create_events(session: Session, count=10):
    """
    Generate multiple events with associated categories, organizers, schedules, and images.
    """
    # Fetch related data
    event_categories, organizers, provinces = fetch_related_data(session)

    cloudinary_service = CloudinaryService()  # Initialize Cloudinary service
    image_root_dir = './seed/seeders/images/events'

    # Generate events
    for _ in range(count):
        create_event(session, cloudinary_service, event_categories, organizers, provinces, image_root_dir)

    print(f"Generated {count} events with schedules, classes, and images.")

def delete_all_events(session: Session):
    """
    Delete all events, their associated images from Cloudinary, and local images.
    """
    cloudinary_service = CloudinaryService()  # Initialize Cloudinary service
    
    cloudinary_service.delete_folder('events')  # Delete all images from the 'events' folder in Cloudinary
    session.query(EventCategoryAssociation).delete()
    session.query(Schedule).delete()
    session.query(EventClass).delete()
    session.query(EventImage).delete()
    session.query(Event).delete()
    
    session.commit()

    print("All events, their images from Cloudinary, and local images have been deleted.")
