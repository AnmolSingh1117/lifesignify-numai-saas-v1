from sqlalchemy.orm import Session
from fastapi import HTTPException
from sqlalchemy.exc import SQLAlchemyError

from app.db.models import User, Organization, Subscription
from app.core.security import (
    hash_password,
    verify_password,
    create_access_token,
)

from app.core.audit import log_action


# =====================================================
# REGISTER (ALWAYS CREATE NEW ORG + BASIC SUBSCRIPTION)
# =====================================================
def create_user(
    db: Session,
    email: str,
    password: str,
    organization_name: str
):
    try:
        # 🔒 Prevent duplicate email
        if db.query(User).filter(User.email == email).first():
            raise HTTPException(status_code=400, detail="Email already registered")

        # 🔒 Prevent joining existing organization (important fix)
        if db.query(Organization).filter(
            Organization.name == organization_name
        ).first():
            raise HTTPException(
                status_code=400,
                detail="Organization name already exists. Please choose a different name."
            )

        # 🏢 Always create new organization
        organization = Organization(
            name=organization_name,
            plan="basic"  # default plan
        )
        db.add(organization)
        db.flush()  # get organization.id

        # 👤 First user is always admin
        user = User(
            email=email,
            password=hash_password(password),
            tenant_id=organization.id,
            role="admin"
        )
        db.add(user)
        db.flush()

        # 🔥 Always create basic subscription
        subscription = Subscription(
            tenant_id=organization.id,
            plan_name="basic",
            is_active=True,
        )
        db.add(subscription)

        db.commit()
        db.refresh(user)

        log_action(
            db=db,
            user_id=user.id,
            tenant_id=user.tenant_id,
            action="USER_REGISTERED",
            details={
                "email": user.email,
                "role": user.role
            }
        )

        return user

    except HTTPException:
        raise

    except SQLAlchemyError:
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail="Database error during registration"
        )


# =====================================================
# AUTHENTICATE USER
# =====================================================
def authenticate_user(db: Session, email: str, password: str):

    user = db.query(User).filter(User.email == email).first()

    if not user:
        return None

    if not verify_password(password, user.password):
        return None

    return user


# =====================================================
# LOGIN (JWT = user + tenant + role)
# =====================================================
def login_user(db: Session, email: str, password: str):

    user = authenticate_user(db, email, password)

    if not user:
        return None

    organization = (
        db.query(Organization)
        .filter(Organization.id == user.tenant_id)
        .first()
    )

    if not organization:
        raise HTTPException(status_code=404, detail="Organization not found")

    token = create_access_token(
        {
            "sub": str(user.id),
            "tenant_id": user.tenant_id,
            "role": user.role,
        }
    )

    log_action(
        db=db,
        user_id=user.id,
        tenant_id=user.tenant_id,
        action="USER_LOGIN",
        details={
            "email": user.email
        }
    )

    return {
        "access_token": token,
        "token_type": "bearer"
    }


# =====================================================
# UPDATE ORGANIZATION PLAN (ADMIN)
# =====================================================
def update_organization_plan(
    db: Session,
    current_user: User,
    new_plan: str
):
    organization = (
        db.query(Organization)
        .filter(Organization.id == current_user.tenant_id)
        .first()
    )

    if not organization:
        raise HTTPException(status_code=404, detail="Organization not found")

    organization.plan = new_plan
    db.commit()
    db.refresh(organization)

    log_action(
        db=db,
        user_id=current_user.id,
        tenant_id=current_user.tenant_id,
        action="PLAN_UPDATED",
        details={
            "new_plan": new_plan
        }
    )

    return organization