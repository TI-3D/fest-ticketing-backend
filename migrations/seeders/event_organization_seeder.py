from app.models import User, EventOrganizer, Provider, Role, UserStatus, ProviderName, OrganizerStatus
from app.core.security import generate_password_hash
from uuid import uuid4
from faker import Faker
from sqlalchemy.orm import Session

fake = Faker()

def create_event_organizer(session: Session, count=5):
    for _ in range(count):
        # Create a new user for event organizer
        user_organizer_id = str(uuid4())
        provider_id = str(uuid4())
        
        user_organizer = User(
            user_id=user_organizer_id,
            full_name=fake.name(),
            email=fake.email(),
            password_hash=generate_password_hash("password"),
            role=Role.EO,
            status=UserStatus.PREMIUM,
            email_verified_at=fake.date_time_this_year(),
            created_at=fake.date_time_this_year(),
            updated_at=fake.date_time_this_year(),
            address=fake.address(),
            phone_number=fake.phone_number(),
            providers=[Provider(
                provider_name=ProviderName.EMAIL,
                user_id=user_organizer_id,
                provider_id=provider_id,
            )],
            organizer=EventOrganizer(
                organizer_id=str(uuid4()),
                company_name=fake.company(),
                company_address=fake.address(),
                status=OrganizerStatus.ACTIVE,
                user_id=user_organizer_id,
                verified_at=fake.date_time_this_year(),
            )
        )
        
        session.add(user_organizer)
    
    session.commit()
    print(f"Generated {count} event organizers.")
