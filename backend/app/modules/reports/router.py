from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.dependencies import get_db
from app.db.models import User, Subscription

from app.modules.users.router import get_current_user, admin_required
from app.modules.reports.schemas import (
    ReportCreate,
    ReportUpdate,
    ReportResponse
)
from app.modules.reports.intake_schema import LifeSignifyRequest

from app.modules.reports.service import (
    create_report,
    create_ai_report,
    get_reports,
    get_report,
    get_radar_data,
    update_report,
    soft_delete_report,
    restore_report,
    hard_delete_report,
    export_report_pdf
)

router = APIRouter(tags=["Reports"])


# =====================================================
# CREATE MANUAL REPORT
# =====================================================
@router.post("/", response_model=ReportResponse)
def create_new_report(
    report: ReportCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return create_report(
        db=db,
        current_user=current_user,
        title=report.title,
        content=report.content
    )


# =====================================================
# 🔥 GENERATE AI REPORT (PRO USERS ONLY)
# =====================================================
@router.post("/generate-ai-report", response_model=ReportResponse)
def generate_ai_report(
    request: LifeSignifyRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    # 🔐 Check Subscription
    subscription = (
        db.query(Subscription)
        .filter(Subscription.user_id == current_user.id)
        .first()
    )

    if not subscription or not subscription.is_active:
        raise HTTPException(
            status_code=403,
            detail="Upgrade to Pro to generate AI reports."
        )

    return create_ai_report(
        db=db,
        current_user=current_user,
        intake_data=request.model_dump()
    )


# =====================================================
# LIST REPORTS
# =====================================================
@router.get("/", response_model=list[ReportResponse])
def list_reports(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return get_reports(
        db=db,
        current_user=current_user
    )


# =====================================================
# GET SINGLE REPORT
# =====================================================
@router.get("/{report_id}", response_model=ReportResponse)
def get_single_report(
    report_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return get_report(
        db=db,
        current_user=current_user,
        report_id=report_id
    )


# =====================================================
# GET RADAR DATA
# =====================================================
@router.get("/{report_id}/radar")
def fetch_radar_data(
    report_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return get_radar_data(
        db=db,
        current_user=current_user,
        report_id=report_id
    )


# =====================================================
# UPDATE REPORT
# =====================================================
@router.put("/{report_id}", response_model=ReportResponse)
def update_existing_report(
    report_id: int,
    report: ReportUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return update_report(
        db=db,
        current_user=current_user,
        report_id=report_id,
        title=report.title,
        content=report.content
    )


# =====================================================
# SOFT DELETE (ADMIN ONLY)
# =====================================================
@router.delete("/{report_id}")
def delete_report(
    report_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(admin_required),
):
    return soft_delete_report(
        db=db,
        current_user=current_user,
        report_id=report_id
    )


# =====================================================
# RESTORE REPORT (ADMIN ONLY)
# =====================================================
@router.put("/{report_id}/restore")
def restore_deleted_report(
    report_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(admin_required),
):
    return restore_report(
        db=db,
        current_user=current_user,
        report_id=report_id
    )


# =====================================================
# HARD DELETE (ADMIN ONLY)
# =====================================================
@router.delete("/{report_id}/hard")
def permanently_delete_report(
    report_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(admin_required),
):
    return hard_delete_report(
        db=db,
        current_user=current_user,
        report_id=report_id
    )


# =====================================================
# EXPORT PDF (PRO ONLY OPTIONAL)
# =====================================================
@router.get("/{report_id}/export-pdf")
def export_pdf(
    report_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return export_report_pdf(
        db=db,
        current_user=current_user,
        report_id=report_id
    )