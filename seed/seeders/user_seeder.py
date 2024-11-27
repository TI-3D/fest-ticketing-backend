import os
import random
from uuid import uuid4
from faker import Faker
from sqlalchemy.orm import Session
from sqlalchemy.sql import select
from app.models import (
    User, EventOrganizer, Provider, Role, Gender,
    OrganizerStatus, ProviderName, Province, City, District, Village, OTP, PersonalAccessToken
)
from app.core.security import generate_password_hash
from app.services.cloudinary_service import CloudinaryService

# Initialize services
fake = Faker()
cloudinary_service = CloudinaryService()  # Initialize Cloudinary service

# Helper function to generate custom phone numbers
def generate_custom_phone_number():
    return '08' + ''.join([str(fake.random_digit()) for _ in range(10)])

# Helper function to generate random nik 16 digit
def generate_unique_nik():
    return ''.join([str(fake.random_digit()) for _ in range(16)])

# Helper function to upload an image to Cloudinary and return the URL
def upload_image_to_cloudinary(image_path: str, folder_name: str):
    return cloudinary_service.upload_image(image_path, folder_name=folder_name)['secure_url']

# Helper function to get random geographical data
def get_random_geographical_data(session: Session):
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
    return selected_province, selected_city, selected_district, selected_village

# Create admin user
def create_user_admin(session: Session):
    image_root_dir = './seed/seeders/images/users'
    image_list = os.listdir(image_root_dir)

    if not image_list:
        print("No images found in the specified directory.")
        return

    image_name = random.choice(image_list)
    image_url = upload_image_to_cloudinary(os.path.join(image_root_dir, image_name), folder_name="profiles")
    
    selected_province, selected_city, selected_district, selected_village = get_random_geographical_data(session)
    
    user_admin = User(
        full_name="Admin",
        email="admin@example.com",
        password_hash=generate_password_hash("password"),
        role=Role.ADMIN,
        gender=(Gender.MALE if fake.boolean() else Gender.FEMALE),
        nik=generate_unique_nik(),
        email_verified_at=fake.date_time_this_year(),
        profile_picture=image_url,
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

# Create a test event organizer
def create_event_organizer_test(session: Session):
    image_root_dir = './seed/seeders/images/users'
    image_list = os.listdir(image_root_dir)

    if not image_list:
        print("No images found in the specified directory.")
        return

    image_name = random.choice(image_list)
    image_url = upload_image_to_cloudinary(os.path.join(image_root_dir, image_name), folder_name="profiles")
    
    organizer_image_root_dir = './seed/seeders/images/event_organizers'
    organizer_image_list = os.listdir(organizer_image_root_dir)

    if not organizer_image_list:
        print("No images found in the specified directory.")
        return

    organizer_image_name = random.choice(organizer_image_list)
    organizer_image_url = upload_image_to_cloudinary(os.path.join(organizer_image_root_dir, organizer_image_name), folder_name="organizers")
    
    selected_province, selected_city, selected_district, selected_village = get_random_geographical_data(session)

    user_organizer = User(
        full_name="Organizer",
        email="eo@example.com",
        password_hash=generate_password_hash("password"),
        role=Role.EO,
        profile_picture=image_url,
        gender=(Gender.MALE if fake.boolean() else Gender.FEMALE),
        nik=generate_unique_nik(),
        email_verified_at=fake.date_time_this_year(),
        address=fake.address(),
        phone_number=generate_custom_phone_number(),
        birth_date=fake.date_of_birth(),
        providers=[Provider(provider_name=ProviderName.EMAIL)],
        province=selected_province,
        city=selected_city,
        district=selected_district,
        village=selected_village,
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
        profile_picture=organizer_image_url,
        address=fake.address()
    )

    session.add(organizer)
    session.commit()
    print("Test event organizer created.")

# Create multiple event organizers
def create_event_organizer(session: Session, count=5):
    image_root_dir = './seed/seeders/images/users'
    image_list = os.listdir(image_root_dir)
    organizer_image_root_dir = './seed/seeders/images/event_organizers'
    organizer_image_list = os.listdir(organizer_image_root_dir)

    if not image_list or not organizer_image_list:
        print("No images found in the specified directories.")
        return

    for _ in range(count):
        image_name = random.choice(image_list)
        image_url = upload_image_to_cloudinary(os.path.join(image_root_dir, image_name), folder_name="profiles")
        organizer_image_name = random.choice(organizer_image_list)
        organizer_image_url = upload_image_to_cloudinary(os.path.join(organizer_image_root_dir, organizer_image_name), folder_name="organizers")
        
        selected_province, selected_city, selected_district, selected_village = get_random_geographical_data(session)

        user_organizer = User(
            full_name=fake.name(),
            email=fake.email(),
            password_hash=generate_password_hash("password"),
            role=Role.EO,
            profile_picture=image_url,
            gender=(Gender.MALE if fake.boolean() else Gender.FEMALE),
            nik=generate_unique_nik(),
            email_verified_at=fake.date_time_this_year(),
            address=fake.address(),
            phone_number=generate_custom_phone_number(),
            birth_date=fake.date_of_birth(),
            providers=[Provider(provider_name=ProviderName.EMAIL)],
            province=selected_province,
            city=selected_city,
            district=selected_district,
            village=selected_village,
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
            profile_picture=organizer_image_url,
            user=user_organizer,
            address=fake.address()
        )

        session.add(organizer)

    session.commit()
    print(f"{count} event organizers created.")

# Create a test user
def create_user_test(session: Session):
    image_root_dir = './seed/seeders/images/users'
    image_list = os.listdir(image_root_dir)

    if not image_list:
        print("No images found in the specified directory.")
        return

    image_name = random.choice(image_list)
    image_url = upload_image_to_cloudinary(os.path.join(image_root_dir, image_name), folder_name="profiles")

    selected_province, selected_city, selected_district, selected_village = get_random_geographical_data(session)

    user_test = User(
        full_name="Test",
        email="test@example.com",
        password_hash=generate_password_hash("password"),
        role=Role.USER,
        gender=(Gender.MALE if fake.boolean() else Gender.FEMALE),
        nik=generate_unique_nik(),
        email_verified_at=fake.date_time_this_year(),
        created_at=fake.date_time_this_year(),
        updated_at=fake.date_time_this_year(),
        address=fake.address(),
        phone_number=generate_custom_phone_number(),
        birth_date=fake.date_of_birth(),
        profile_picture=image_url,
        providers=[Provider(provider_name=ProviderName.EMAIL)],
        province=selected_province,
        city=selected_city,
        district=selected_district,
        village=selected_village
    )

    session.add(user_test)
    session.commit()
    print("Test user created.")

# Create multiple users
def create_users(session: Session, count=10):
    image_root_dir = './seed/seeders/images/users'
    image_list = os.listdir(image_root_dir)

    if not image_list:
        print("No images found in the specified directory.")
        return

    for _ in range(count):
        image_name = random.choice(image_list)
        image_url = upload_image_to_cloudinary(os.path.join(image_root_dir, image_name), folder_name="profiles")
        
        selected_province, selected_city, selected_district, selected_village = get_random_geographical_data(session)

        user = User(
            full_name=fake.name(),
            email=fake.email(),
            password_hash=generate_password_hash("password"),
            role=Role.USER,
            nik=generate_unique_nik(),
            gender=(Gender.MALE if fake.boolean() else Gender.FEMALE),
            email_verified_at=fake.date_time_this_year(),
            created_at=fake.date_time_this_year(),
            updated_at=fake.date_time_this_year(),
            address=fake.address(),
            phone_number=generate_custom_phone_number(),
            birth_date=fake.date_of_birth(),
            profile_picture=image_url,
            providers=[Provider(provider_name=ProviderName.EMAIL)],
            province=selected_province,
            city=selected_city,
            district=selected_district,
            village=selected_village
        )

        session.add(user)

    session.commit()
    print(f"Generated {count} users.")

# Delete all users and associated data
def delete_all_users(session: Session):
    cloudinary_service.delete_folder("profiles")
    cloudinary_service.delete_folder("organizers")
    
    session.query(PersonalAccessToken).delete()
    session.query(OTP).delete()
    session.query(Provider).delete()
    session.query(EventOrganizer).delete()
    session.query(User).delete()
    session.commit()
    print("All users and associated data deleted.")
