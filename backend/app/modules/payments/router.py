from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from pydantic import BaseModel

from app.db.dependencies import get_db
from app.modules.users.router import get_current_user
from app.db.models import User
from app.modules.payments.service import (
    create_payment_order,
    verify_payment_signature
)

router = APIRouter(tags=["Payments"])


# =====================================================
# REQUEST MODEL FOR VERIFY
# =====================================================
class VerifyPaymentRequest(BaseModel):
    razorpay_order_id: str
    razorpay_payment_id: str
    razorpay_signature: str


# =====================================================
# CREATE ORDER
# =====================================================
@router.post("/create-order")
def create_order(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return create_payment_order(db, current_user)


# =====================================================
# VERIFY PAYMENT (JSON BODY VERSION)
# =====================================================
@router.post("/verify")
def verify_payment(
    payload: VerifyPaymentRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return verify_payment_signature(
        db=db,
        current_user=current_user,
        razorpay_order_id=payload.razorpay_order_id,
        razorpay_payment_id=payload.razorpay_payment_id,
        razorpay_signature=payload.razorpay_signature,
    )