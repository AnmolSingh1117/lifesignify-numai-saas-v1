from sqlalchemy.orm import Session
from fastapi import HTTPException
from sqlalchemy.exc import SQLAlchemyError

from app.db.models import User, Organization
from app.core.security import (
    hash_password,
    verify_password,
    create_access_token,
)

from app.core.audit import log_action


# =====================================================
# REGISTER (Create User inside Organization)
# =====================================================
def create_user(
    db: Session,
    email: str,
    password: str,
    organization_name: str
):
    try:
        if (
            db.query(User)
            .filter(User.email == email, User.is_deleted == False)
            .first()
        ):
            raise HTTPException(status_code=400, detail="Email already registered")

        organization = (
            db.query(Organization)
            .filter(
                Organization.name == organization_name,
                Organization.is_deleted == False
            )
            .first()
        )

        is_new_org = False

        if not organization:
            organization = Organization(
                name=organization_name,
                plan="free"
            )
            db.add(organization)
            db.flush()
            is_new_org = True

        role = "admin" if is_new_org else "user"

        user = User(
            email=email,
            password=hash_password(password),
            tenant_id=organization.id,
            role=role
        )

        db.add(user)
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
# AUTHENTICATE USER (Soft Delete Aware)
# =====================================================
def authenticate_user(db: Session, email: str, password: str):

    user = (
        db.query(User)
        .filter(
            User.email == email,
            User.is_deleted == False
        )
        .first()
    )

    if not user:
        return None

    if not verify_password(password, user.password):
        return None

    return user


# =====================================================
# LOGIN (JWT contains tenant_id + role ONLY)
# =====================================================
def login_user(db: Session, email: str, password: str):

    user = authenticate_user(db, email, password)

    if not user:
        return None

    organization = (
        db.query(Organization)
        .filter(
            Organization.id == user.tenant_id,
            Organization.is_deleted == False
        )
        .first()
    )

    if not organization:
        raise HTTPException(status_code=404, detail="Organization not found")

    # ✅ Removed plan from JWT
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
# UPDATE ORGANIZATION PLAN (Admin Only)
# =====================================================
def update_organization_plan(
    db: Session,
    current_user: User,
    new_plan: str
):
    organization = (
        db.query(Organization)
        .filter(
            Organization.id == current_user.tenant_id,
            Organization.is_deleted == False
        )
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