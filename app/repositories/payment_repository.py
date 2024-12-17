from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update
from app.models import Payment, PaymentStatus
from app.core.config import Logger
from typing import List, Optional
from sqlalchemy.orm import joinedload

class PaymentRepository:
    def __init__(self, session: AsyncSession):
        self.session = session
        self.logger = Logger(__name__).get_logger()

    async def get_all_payments(self, user_id:str) -> List[Payment]:
        """
        Retrieve all payments.
        """
        try:
            self.logger.info("Attempting to retrieve all payments")
            result = await self.session.execute(
                select(Payment)
                .filter(Payment.user_id == user_id)
                .options(joinedload(Payment.user))
                .options(joinedload(Payment.event))
                .options(joinedload(Payment.event_class))
                .order_by(Payment.updated_at.desc())
            )
            payments = result.scalars().all()
            return payments
        except Exception as e:
            self.logger.error(f"Error retrieving all payments: {str(e)}")
            raise

    async def get_payment_by_id(self, user_id, payment_id: str) -> Optional[Payment]:
        """
        Retrieve a payment by its ID.
        """
        try:
            self.logger.info(f"Retrieving payment with ID: {payment_id}")
            result = await self.session.execute(
                select(Payment)
                .filter(Payment.user_id == user_id)
                .options(joinedload(Payment.user))
                .options(joinedload(Payment.event))
                .options(joinedload(Payment.event_class))
                .order_by(Payment.updated_at.desc()
                .filter(Payment.payment_id == payment_id)
            ))
            payment = result.scalars().first()
            return payment
        except Exception as e:
            self.logger.error(f"Error retrieving payment by ID {payment_id}: {str(e)}")
            raise

    async def create_payment(self, payment: Payment) -> Payment:
        """
        Create a new payment.
        """
        try:
            self.logger.info("Creating new payment")
            self.session.add(payment)
            await self.session.commit()
            self.logger.info(f"Created payment with ID: {payment.payment_id}")
            return payment
        except Exception as e:
            self.logger.error(f"Error creating payment: {str(e)}")
            raise

    async def update_payment(self, payment_id: str, update_data: dict) -> bool:
        """
        Update an existing payment.
        """
        try:
            self.logger.info(f"Updating payment with ID: {payment_id}")
            stmt = update(Payment).where(Payment.payment_id == payment_id).values(**update_data)
            result = await self.session.execute(stmt)
            if result.rowcount == 0:
                self.logger.warning(f"Payment with ID {payment_id} not found for update.")
                return False
            
            self.logger.info(f"Updated payment with ID: {payment_id}")
            return True
        except Exception as e:
            self.logger.error(f"Error updating payment with ID {payment_id}: {str(e)}")
            raise
        
    async def update_payment_status(self, payment_id: str, new_status: PaymentStatus) -> bool:
        """
        Update the status of a payment.
        """
        try:
            self.logger.info(f"Updating status of payment with ID: {payment_id}")
            stmt = update(Payment).where(Payment.payment_id == payment_id).values(payment_status=new_status)
            result = await self.session.execute(stmt)
            if result.rowcount == 0:
                self.logger.warning(f"Payment with ID {payment_id} not found for status update.")
                return False
            
            self.logger.info(f"Updated status of payment with ID: {payment_id}")
            return True
        except Exception as e:
            self.logger.error(f"Error updating status of payment with ID {payment_id}: {str(e)}")
            raise

    async def delete_payment(self, payment_id: str) -> bool:
        """
        Delete a payment by ID.
        """
        try:
            payment = await self.get_payment_by_id(payment_id)
            if not payment:
                self.logger.warning(f"Payment with ID {payment_id} not found")
                return False

            await self.session.delete(payment)
            await self.session.commit()
            self.logger.info(f"Deleted payment with ID: {payment_id}")
            return True
        except Exception as e:
            self.logger.error(f"Error deleting payment with ID {payment_id}: {str(e)}")
            raise