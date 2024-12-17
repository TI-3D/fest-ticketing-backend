from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException
from app.models import Payment
from app.repositories import PaymentRepository
from app.schemas.payment import PaymentRequest, PaymentResponse, PaymentStatusUpdate
from app.core.config import Logger
from typing import Dict, List
from datetime import datetime

class PaymentService:
    def __init__(self, session: AsyncSession):
        self.payment_repository = PaymentRepository(session)
        self.session = session
        self.logger = Logger(__name__).get_logger()

    async def get_all_payments(self, current: Dict) -> List[PaymentResponse]:
        async with self.session.begin():
            self.logger.info("Retrieving all payments")
            payments = await self.payment_repository.get_all_payments(current['sub'])
            return [PaymentResponse.model_validate(payment) for payment in payments]

    async def get_payment_by_id(self, current: Dict, payment_id: str,) -> PaymentResponse:
        async with self.session.begin():
            self.logger.info(f"Retrieving payment {payment_id}")
            payment = await self.payment_repository.get_payment_by_id(current['sub'], payment_id)
            if not payment:
                self.logger.warning(f"Payment {payment_id} not found")
                raise HTTPException(status_code=404, detail="Payment not found")
            return PaymentResponse.model_validate(payment)

    async def create_payment(self, payment_request: PaymentRequest, current: Dict) -> PaymentResponse:
        async with self.session.begin():
            self.logger.info(f"Creating payment for user {current.get('sub')}")
            payment = Payment(
                amount=payment_request.amount,
                qty=payment_request.qty,
                total=payment_request.total,
                date=datetime.now(),
                payment_status="PENDING",  # Status default
                event_id=payment_request.event_id,
                event_class_id=payment_request.event_class_id,
                user_id=current['sub']
            )
            created_payment = await self.payment_repository.create_payment(payment)
            return PaymentResponse.model_validate(created_payment)

    async def update_payment_status(self, payment_id: str, status_update: PaymentStatusUpdate, current: Dict) -> PaymentResponse:
        async with self.session.begin():
            self.logger.info(f"Updating status of payment {payment_id}")
            payment = await self.payment_repository.get_payment_by_id(current['sub'], payment_id)
            if not payment:
                self.logger.warning(f"Payment {payment_id} not found")
                raise HTTPException(status_code=404, detail="Payment not found")
            update_data = {"payment_status": status_update.payment_status}
            await self.payment_repository.update_payment(payment_id, update_data)
            payment.payment_status = status_update.payment_status  # Update status in the response
            return PaymentResponse.model_validate(payment)