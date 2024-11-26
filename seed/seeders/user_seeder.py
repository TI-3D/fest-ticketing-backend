from faker import Faker
from uuid import uuid4
from sqlalchemy.orm import Session
from app.models import (
    User, EventOrganizer, Provider, Role, UserStatus, Gender,
    OrganizerStatus, ProviderName, Province, City, District, Village, OTP, PersonalAccessToken
)
from app.core.security import generate_password_hash
import random
from sqlalchemy.sql import select
import os
from app.services.cloudinary_service import CloudinaryService

cloudinary_service = CloudinaryService()  # Initialize the Cloudinary service
fake = Faker()

def generate_custom_phone_number():
    return '08' + ''.join([str(fake.random_digit()) for _ in range(10)])

def create_user_admin(session: Session):
    provinces = session.execute(select(Province)).scalars().all()
    # Directory containing user images
    image_root_dir = './seed/seeders/images/users'
    
    # Read all image in user images directory
    image_list = os.listdir(image_root_dir)
    
    # Ensure there are images available to use
    if not image_list:
        print("No images found in the specified directory.")
        return
    
    # Randomly select an image from the list
    image_name = random.choice(image_list)
    
    # Upload the selected image to Cloudinary
    image_url = cloudinary_service.upload_image(os.path.join(image_root_dir, image_name), folder_name="profiles")
    
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
    
    user_admin = User(
        full_name="Admin",
        email="admin@example.com",
        password_hash=generate_password_hash("password"),
        role=Role.ADMIN,
        status=UserStatus.PREMIUM,
        gender=Gender.MALE,
        email_verified_at=fake.date_time_this_year(),
        profile_picture=image_url['secure_url'],
        created_at=fake.date_time_this_year(),
        updated_at=fake.date_time_this_year(),
        address=fake.address(),
        phone_number=generate_custom_phone_number(),
        birth_date=fake.date_of_birth(),
        providers=[Provider(provider_name=ProviderName.EMAIL)],
        province=selected_province,
        city=selected_city,
        district=selected_district,
        village=selected_village
    )
    session.add(user_admin)
    session.commit()
    print("Admin user created.")
    
def create_event_organizer_test(session: Session):
    provinces = session.execute(select(Province)).scalars().all()
    
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
    
    # Directory containing user images
    image_root_dir = './seed/seeders/images/users'
    
    # Read all image in user images directory
    image_list = os.listdir(image_root_dir)
    
    # Ensure there are images available to use
    if not image_list:
        print("No images found in the specified directory.")
        return
    
    # Randomly select an image from the list
    image_name = random.choice(image_list)
    
    # Upload the selected image to Cloudinary
    image_url = cloudinary_service.upload_image(os.path.join(image_root_dir, image_name), folder_name="profiles")
    
    # Directory containing event organizer images
    organizer_image_root_dir = './seed/seeders/images/event_organizers'
    
    # Read all image in event organizer images directory
    organizer_image_list = os.listdir(organizer_image_root_dir)
    
    # Ensure there are images available to use
    if not organizer_image_list:
        print("No images found in the specified directory.")
        return
    
    # Randomly select an image from the list
    organizer_image_name = random.choice(organizer_image_list)
    
    # Upload the selected image to Cloudinary
    organizer_image_url = cloudinary_service.upload_image(os.path.join(organizer_image_root_dir, organizer_image_name), folder_name="organizers")
    
    user_selected_province = random.choice(provinces)
    user_selected_city = random.choice(
        session.execute(select(City).where(City.code_province == user_selected_province.code_province)).scalars().all()
    )
    user_selected_district = random.choice(
        session.execute(select(District).where(District.code_city == user_selected_city.code_city)).scalars().all()
    )
    user_selected_village = random.choice(
        session.execute(select(Village).where(Village.code_district == user_selected_district.code_district)).scalars().all()
    )
    
    user_organizer = User(
        full_name="Organizer",
        email="eo@example.com",
        password_hash=generate_password_hash("password"),
        role=Role.EO,
        status=UserStatus.PREMIUM,
        profile_picture=image_url['secure_url'],
        gender=fake.random_element(list(Gender)),
        email_verified_at=fake.date_time_this_year(),
        address=fake.address(),
        phone_number=generate_custom_phone_number(),
        birth_date=fake.date_of_birth(),
        providers=[Provider(provider_name=ProviderName.EMAIL)],
        province=user_selected_province,
        city=user_selected_city,
        district=user_selected_district,
        village=user_selected_village
        )

    organizer = EventOrganizer(
        organizer_id=uuid4(),
        company_name=fake.company(),
        company_address=fake.address(),
        status=OrganizerStatus.ACTIVE,
        verified_at=fake.date_time_this_year(),
        province=selected_province,
        city=selected_city,
        district=selected_district,
        village=selected_village,
        user=user_organizer,
        profile_picture=organizer_image_url['secure_url']
    )
    session.add(organizer)
    session.commit()
    print(f"Test event organizer created.")

def create_event_organizer(session: Session, count=5):
    provinces = session.execute(select(Province)).scalars().all()
    
    # Directory containing user images
    image_root_dir = './seed/seeders/images/users'
    
    # Read all image in user images directory
    image_list = os.listdir(image_root_dir)
    
    organizer_image_root_dir = './seed/seeders/images/event_organizers'
    organizer_image_list = os.listdir(organizer_image_root_dir)
    
    # Ensure there are images available to use
    if not image_list:
        print("No images found in the specified directory.")
        return
    
    if not organizer_image_list:
        print("No images found in the specified directory.")
        return
    
    
    for _ in range(count):
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
        
        # Randomly select an image from the list
        image_name = random.choice(image_list)
        
        # Upload the selected image to Cloudinary
        image_url = cloudinary_service.upload_image(os.path.join(image_root_dir, image_name), folder_name="profiles")
        
        # Randomly select an image from the list
        organizer_image_name = random.choice(organizer_image_list)
        
        # Upload the selected image to Cloudinary
        organizer_image_url = cloudinary_service.upload_image(os.path.join(organizer_image_root_dir, organizer_image_name), folder_name="organiers")
        
        user_selected_province = random.choice(provinces)
        user_selected_city = random.choice(
            session.execute(select(City).where(City.code_province == user_selected_province.code_province)).scalars().all()
        )
        user_selected_district = random.choice(
            session.execute(select(District).where(District.code_city == user_selected_city.code_city)).scalars().all()
        )
        user_selected_village = random.choice(
            session.execute(select(Village).where(Village.code_district == user_selected_district.code_district)).scalars().all()
        )

        user_organizer = User(
            full_name=fake.name(),
            email=fake.email(),
            password_hash=generate_password_hash("password"),
            role=Role.EO,
            status=UserStatus.PREMIUM,
            gender=fake.random_element(list(Gender)),
            email_verified_at=fake.date_time_this_year(),
            address=fake.address(),
            phone_number=generate_custom_phone_number(),
            birth_date=fake.date_of_birth(),
            profile_picture=image_url['secure_url'],
            providers=[Provider(provider_name=ProviderName.EMAIL)],
            province=user_selected_province,
            city=user_selected_city,
            district=user_selected_district,
            village=user_selected_village
        )

        organizer = EventOrganizer(
            organizer_id=uuid4(),
            company_name=fake.company(),
            company_address=fake.address(),
            status=OrganizerStatus.ACTIVE,
            verified_at=fake.date_time_this_year(),
            province=selected_province,
            city=selected_city,
            district=selected_district,
            village=selected_village,
            profile_picture=organizer_image_url['secure_url'],
            user=user_organizer
        )
        session.add(organizer)
    session.commit()
    print(f"{count} event organizers created.")

def create_user_test(session: Session):
    provinces = session.execute(select(Province)).scalars().all()
    # Directory containing user images
    image_root_dir = './seed/seeders/images/users'
    
    # Read all image in user images directory
    image_list = os.listdir(image_root_dir)
    
    # Ensure there are images available to use
    if not image_list:
        print("No images found in the specified directory.")
        return
    
    # Randomly select an image from the list
    image_name = random.choice(image_list)
    
    # Upload the selected image to Cloudinary
    image_url = cloudinary_service.upload_image(os.path.join(image_root_dir, image_name), folder_name="profiles")
    
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
    
    user_test = User(
        full_name="Test",
        email="test@example.com",
        password_hash=generate_password_hash("password"),
        role=Role.USER,
        status=UserStatus.BASIC,
        email_verified_at=fake.date_time_this_year(),
        created_at=fake.date_time_this_year(),
        updated_at=fake.date_time_this_year(),
        address=fake.address(),
        phone_number=generate_custom_phone_number(),
        birth_date=fake.date_of_birth(),
        profile_picture=image_url['secure_url'],
        providers=[Provider(
            provider_name=ProviderName.EMAIL,
        )],   
        province=selected_province,
        city=selected_city,
        district=selected_district,
        village=selected_village
    )
    
    session.add(user_test)
    session.commit()
    print("Test user created.")
    
def create_users(session: Session, count=10):
    provinces = session.execute(select(Province)).scalars().all()
    # Directory containing user images
    image_root_dir = './seed/seeders/images/users'
    
    # Read all image in user images directory
    image_list = os.listdir(image_root_dir)
    
    # Ensure there are images available to use
    if not image_list:
        print("No images found in the specified directory.")
        return
    
    
    for _ in range(count):
        
        # Randomly select an image from the list
        image_name = random.choice(image_list)
        
        # Upload the selected image to Cloudinary
        image_url = cloudinary_service.upload_image(os.path.join(image_root_dir, image_name), folder_name="profiles")
        user_selected_province = random.choice(provinces)
        user_selected_city = random.choice(
            session.execute(select(City).where(City.code_province == user_selected_province.code_province)).scalars().all()
        )
        user_selected_district = random.choice(
            session.execute(select(District).where(District.code_city == user_selected_city.code_city)).scalars().all()
        )
        user_selected_village = random.choice(
            session.execute(select(Village).where(Village.code_district == user_selected_district.code_district)).scalars().all()
        )
        user = User(
            full_name=fake.name(),
            email=fake.email(),
            password_hash=generate_password_hash("password"),
            role=Role.USER,
            status=UserStatus.BASIC,
            email_verified_at=fake.date_time_this_year(),
            created_at=fake.date_time_this_year(),
            updated_at=fake.date_time_this_year(),
            address=fake.address(),
            phone_number=generate_custom_phone_number(),
            birth_date=fake.date_of_birth(),
            profile_picture=image_url['secure_url'],
            providers=[Provider(
                provider_name=ProviderName.EMAIL,
            )],
            province=user_selected_province,
            city=user_selected_city,
            district=user_selected_district,
            village=user_selected_village
        )
        session.add(user)
    session.commit()
    print(f"Generated {count} users.")
    
def delete_all_users(session: Session):
    
    # Delete all data from the database
    cloudinary_service.delete_folder("profiles")
    
    cloudinary_service.delete_folder("organizers")
    
    session.query(PersonalAccessToken).delete()
    session.query(OTP).delete()
    session.query(Provider).delete()
    session.query(EventOrganizer).delete()
    session.query(User).delete()
    session.commit()
    print("All users deleted.")