from sqlalchemy.orm import Session
from app.models import (
    Event, EventCategories, EventOrganizer, EventClass, EventStatus,
    EventCategoryAssociation, Schedule, DayOfWeek, Province, City, District, Village, EventImage
)
import random
from faker import Faker
from sqlalchemy.sql import select
from datetime import timedelta, datetime
import os
from app.services.cloudinary_service import CloudinaryService

fake = Faker()

from sqlalchemy.orm import Session
from app.models import (
    Event, EventCategories, EventOrganizer, EventClass, EventStatus,
    EventCategoryAssociation, Schedule, DayOfWeek, Province, City, District, Village, EventImage
)
from app.services.cloudinary_service import CloudinaryService
import random
from faker import Faker
from sqlalchemy.sql import select
from datetime import timedelta, datetime
import os

fake = Faker()

def create_events(session: Session, count=10):
    """
    Generate events with random categories, organizers, administrative region codes, schedules,
    and upload images for each event.
    """
    # Fetch related data
    event_categories = session.execute(select(EventCategories)).scalars().all()
    organizers = session.execute(select(EventOrganizer)).scalars().all()
    provinces = session.execute(select(Province)).scalars().all()

    cloudinary_service = CloudinaryService()  # Initialize the Cloudinary service
    
    # Directory containing event images
    image_root_dir = './seed/seeders/images/events'

    # Read all folders in the specified directory
    folder_list = os.listdir(image_root_dir)
    
    # Ensure there are folders available to use
    if not folder_list:
        print("No folders found in the specified directory.")
        return

    
    for index in range(count):
        # Randomly select organizer and administrative regions
        selected_organizer = random.choice(organizers)
        selected_province = random.choice(provinces)
        selected_city = random.choice(
            session.execute(select(City).where(City.code_province == selected_province.code_province)).scalars().all()
        )
        selected_district = random.choice(
            session.execute(select(District).where(District.code_city == selected_city.code_city)).scalars().all()
        )
        selected_village = random.choice(
            session.execute(select(Village).where(Village.code_district == selected_district.code_district)).scalars().all()
        )
        selected_categories = random.sample(event_categories, random.randint(1, 3))  # Select 1-3 categories

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

        # Upload images from the folders
        folder_name = folder_list[index % len(folder_list)]  # Cycle through the folders
        folder_path = os.path.join(image_root_dir, folder_name)
        
        if os.path.isdir(folder_path):  # Ensure it's a folder
            for image_file in os.listdir(folder_path):
                if image_file.lower().endswith(('.jpg', '.jpeg', '.png')):  # Filter by image types
                    image_path = os.path.join(folder_path, image_file)
                    
                    # Upload image to Cloudinary
                    image_url = cloudinary_service.upload_image(image_path, folder_name='events')
                    
                    # If the upload is successful, link the image to the event
                    if image_url:
                        event_image = EventImage(
                            event_id=event.event_id,
                            image_url=image_url['secure_url'],  # Store the secure URL
                        )
                        session.add(event_image)

        session.commit()

    print(f"Generated {count} events with schedules, classes, and images.")

def delete_all_events(session: Session):
    """
    Delete all events from the database, their associated images from Cloudinary,
    and clean up the local event image directory.
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
