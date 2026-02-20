from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.db.models import Payment, User, Subscription, Organization
from app.core.payment_config import razorpay_client
from datetime import datetime
import hmac
import hashlib


# =====================================================
# CREATE RAZORPAY ORDER
# =====================================================
def create_payment_order(db: Session, current_user: User):

    amount = 49900  # ₹499 in paise

    order = razorpay_client.order.create({
        "amount": amount,
        "currency": "INR",
        "payment_capture": 1
    })

    payment = Payment(
        user_id=current_user.id,
        tenant_id=current_user.tenant_id,
        razorpay_order_id=order["id"],
        amount=amount,
        currency="INR",
        status="created",
        created_at=datetime.utcnow()
    )

    db.add(payment)
    db.commit()
    db.refresh(payment)

    return {
        "order_id": order["id"],
        "amount": amount,
        "key": razorpay_client.auth[0]  # Key ID
    }


# =====================================================
# VERIFY PAYMENT SIGNATURE + ACTIVATE SUBSCRIPTION
# =====================================================
def verify_payment_signature(
    db: Session,
    current_user: User,
    razorpay_order_id: str,
    razorpay_payment_id: str,
    razorpay_signature: str,
):

    print("---------- VERIFY START ----------")
    print("Order ID:", razorpay_order_id)
    print("Payment ID:", razorpay_payment_id)
    print("Signature:", razorpay_signature)

    try:
        # =====================================================
        # Get Secret From Razorpay Client
        # =====================================================
        razorpay_secret = razorpay_client.auth[1]

        if not razorpay_secret:
            raise Exception("Razorpay secret not configured")

        print("Secret Loaded:", razorpay_secret)

        # =====================================================
        # Generate Signature
        # =====================================================
        generated_signature = hmac.new(
            razorpay_secret.encode("utf-8"),
            f"{razorpay_order_id}|{razorpay_payment_id}".encode("utf-8"),
            hashlib.sha256
        ).hexdigest()

        print("Generated Signature:", generated_signature)

        # =====================================================
        # Validate Signature
        # =====================================================
        if generated_signature != razorpay_signature:
            raise Exception("Signature mismatch")

        print("✅ Signature verified")

        # =====================================================
        # Validate Payment Record Exists
        # =====================================================
        payment = (
            db.query(Payment)
            .filter(Payment.razorpay_order_id == razorpay_order_id)
            .first()
        )

        print("Payment Found:", payment is not None)

        if not payment:
            raise Exception("Payment order not found in DB")

        # Prevent duplicate activation
        if payment.status == "paid":
            print("Payment already verified")
            return {
                "message": "Payment already verified.",
                "plan": "pro"
            }

        payment.status = "paid"
        payment.razorpay_payment_id = razorpay_payment_id

        # =====================================================
        # Activate Subscription (Aligned With Your Model)
        # =====================================================
        subscription = (
            db.query(Subscription)
            .filter(Subscription.user_id == current_user.id)
            .first()
        )

        if subscription:
            subscription.is_active = True
        else:
            subscription = Subscription(
                user_id=current_user.id,
                is_active=True
            )
            db.add(subscription)

        # =====================================================
        # Update Organization Plan
        # =====================================================
        organization = (
            db.query(Organization)
            .filter(Organization.id == current_user.tenant_id)
            .first()
        )

        if organization:
            organization.plan = "pro"

        db.commit()

        print("🎉 Subscription activated successfully")
        print("---------- VERIFY SUCCESS ----------")

        return {
            "message": "Payment verified. Subscription activated.",
            "plan": "pro"
        }

    except Exception as e:
        print("🔥 VERIFY ERROR:", str(e))
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )