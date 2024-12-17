import random
from datetime import datetime
from sqlalchemy.orm import Session
from sqlalchemy.sql import select
from faker import Faker
from app.models import Payment, User, Event, EventClass, PaymentStatus, PaymentMethodType

fake = Faker()

def fetch_related_data(session: Session):
    """
    Fetch users, events, and event classes from the database.
    """
    users = session.execute(select(User)).scalars().all()
    events = session.execute(select(Event)).scalars().all()
    event_classes = session.execute(select(EventClass)).scalars().all()
    return users, events, event_classes

def create_payment(session: Session, users, events, event_classes):
    """
    Create a single payment with associated user, event, and event class.
    """
    selected_user = random.choice(users)
    selected_event = random.choice(events)
    selected_event_class = random.choice(event_classes)

    # Generate random quantity and total amount
    qty = random.randint(1, 5)
    total = selected_event_class.base_price * qty

    # Create the payment
    payment = Payment(
        amount=selected_event_class.base_price,
        qty=qty,
        total=total,
        date=datetime.now(),
        payment_status=random.choice(list(PaymentStatus)),
        payment_method=random.choice(list(PaymentMethodType)),
        user_id=selected_user.user_id,
        event_id=selected_event.event_id,
        event_class_id=selected_event_class.event_class_id,
    )
    session.add(payment)

def create_payments(session: Session, count=10):
    """
    Generate multiple payments with associated users, events, and event classes.
    """
    # Fetch related data
    users, events, event_classes = fetch_related_data(session)

    # Generate payments
    for _ in range(count):
        create_payment(session, users, events, event_classes)

    session.commit()  # Commit all payments at once
    print(f"Generated {count} payments.")

def delete_all_payments(session: Session):
    """
    Delete all payments from the database.
    """
    session.query(Payment).delete()
    session.commit()
    print("All payments have been deleted.")