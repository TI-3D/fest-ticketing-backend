from fastapi import APIRouter, Depends, HTTPException
from app.dependencies.database import get_db
from app.dependencies.auth import get_current_user
from app.schemas.payment import PaymentRequest, PaymentResponse, PaymentStatusUpdate
from app.services.payment_service import PaymentService
from typing import List, Dict, Optional
from app.core.config import Logger

router = APIRouter()
logger = Logger(__name__).get_logger()

@router.get("/", response_model=List[PaymentResponse])
async def get_all_payments(
    db=Depends(get_db),
    current_user: Dict = Depends(get_current_user)
):
    """
    Endpoint untuk mendapatkan semua pembayaran.
    """
    service = PaymentService(db)
    logger.debug("Received request to get all payments")
    try:
        response = await service.get_all_payments(current_user)
        logger.info("All payments have been retrieved successfully")
        return response
    except HTTPException as e:
        logger.error(f"Error while getting all payments: {e}")
        raise e
    except Exception as e:
        logger.error(f"Error while getting all payments: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/{payment_id}", response_model=PaymentResponse)
async def get_payment_by_id(
    payment_id: str,
    db=Depends(get_db),
    current_user: Dict = Depends(get_current_user)
):
    """
    Endpoint untuk mendapatkan pembayaran berdasarkan ID.
    """
    service = PaymentService(db)
    logger.debug(f"Received request to get payment {payment_id}")
    try:
        response = await service.get_payment_by_id(payment_id, current_user)
        logger.info(f"Payment {payment_id} has been retrieved successfully")
        return response
    except HTTPException as e:
        logger.error(f"Error while getting payment: {e}")
        raise e
    except Exception as e:
        logger.error(f"Error while getting payment: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/", response_model=PaymentResponse, status_code=201)
async def create_payment(
    payment_request: PaymentRequest,
    db=Depends(get_db),
    current_user: Dict = Depends(get_current_user)
):
    """
    Endpoint untuk membuat pembayaran baru.
    """
    service = PaymentService(db)
    logger.debug(f"Received request to create payment for user {current_user.get('sub')}")
    try:
        response = await service.create_payment(payment_request, current_user)
        logger.info(f"Payment created successfully for user {current_user.get('sub')}")
        return response
    except HTTPException as e:
        logger.error(f"Error while creating payment: {e}")
        raise e
    except Exception as e:
        logger.error(f"Error while creating payment: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.patch("/{payment_id}/status", response_model=PaymentResponse)
async def update_payment_status(
    payment_id: str,
    status_update: PaymentStatusUpdate,
    db=Depends(get_db),
    current_user: Dict = Depends(get_current_user)
):
    """
    Endpoint untuk memperbarui status pembayaran.
    """
    service = PaymentService(db)
    logger.debug(f"Received request to update status of payment {payment_id}")
    try:
        response = await service.update_payment_status(payment_id, status_update, current_user)
        logger.info(f"Status of payment {payment_id} has been updated successfully")
        return response
    except HTTPException as e:
        logger.error(f"Error while updating payment status: {e}")
        raise e
    except Exception as e:
        logger.error(f"Error while updating payment status: {e}")
        raise HTTPException(status_code=500, detail=str(e))