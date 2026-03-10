from pydantic import BaseModel, Field
from typing import Optional, List, Literal


# =========================================================
# I. CORE IDENTITY (NUMEROLOGY FOUNDATION)
# =========================================================

class BasicIdentity(BaseModel):
    full_name: str = Field(..., min_length=2)
    date_of_birth: str  # YYYY-MM-DD recommended
    gender: Optional[Literal["male", "female", "other"]] = None
    country_of_residence: str = Field(..., min_length=2)

    # 🔥 Added for hybrid systems
    email: Optional[str] = None
    partner_name: Optional[str] = None
    business_name: Optional[str] = None


class BirthDetails(BaseModel):
    date_of_birth: str
    time_of_birth: Optional[str] = None
    birthplace_city: Optional[str] = None
    birthplace_country: Optional[str] = None


class FocusArea(BaseModel):
    life_focus: Literal[
        "finance_debt",
        "career_growth",
        "relationship",
        "health_stability",
        "emotional_confusion",
        "business_decision",
        "general_alignment"
    ]


class ContactLayer(BaseModel):
    mobile_number: Optional[str] = None


# =========================================================
# II. BEHAVIORAL / SCORING LAYER
# =========================================================

class FinancialSnapshot(BaseModel):
    monthly_income: Optional[int] = None
    savings_ratio: Optional[int] = Field(None, ge=0, le=100)
    debt_ratio: Optional[int] = Field(None, ge=0, le=100)
    risk_tolerance: Optional[Literal["low", "moderate", "high"]] = None


class CareerProfile(BaseModel):
    industry: Optional[str] = None
    role: Optional[Literal["entrepreneur", "employee", "consultant", "student"]] = None
    years_experience: Optional[int] = None
    stress_level: Optional[int] = Field(None, ge=1, le=10)


class EmotionalState(BaseModel):
    anxiety_level: Optional[int] = Field(None, ge=1, le=10)
    decision_confusion: Optional[int] = Field(None, ge=1, le=10)
    impulse_control: Optional[int] = Field(None, ge=1, le=10)
    emotional_stability: Optional[int] = Field(None, ge=1, le=10)


# =========================================================
# III. PREMIUM / ADVANCED INPUTS
# =========================================================

class LifeEvents(BaseModel):
    positive_events_years: Optional[List[int]] = None
    setback_events_years: Optional[List[int]] = None


class BusinessHistory(BaseModel):
    major_investments: Optional[int] = None
    major_losses: Optional[int] = None
    risk_mistakes_count: Optional[int] = None


class HealthLifestyle(BaseModel):
    sleep_hours: Optional[int] = None
    alcohol: Optional[bool] = None
    smoking: Optional[bool] = None
    exercise_frequency_per_week: Optional[int] = None
    food_pattern: Optional[Literal["veg", "non_veg", "mixed"]] = None


# =========================================================
# AI CALIBRATION LAYER
# =========================================================

class CalibrationAnswers(BaseModel):

    stress_response: Optional[
        Literal["withdraw", "impulsive", "overthink", "take_control"]
    ] = None

    money_decision_style: Optional[
        Literal["emotional", "calculated", "risky", "avoidant"]
    ] = None

    biggest_weakness: Optional[
        Literal["discipline", "patience", "confidence", "focus"]
    ] = None

    life_preference: Optional[
        Literal["stability", "growth", "recognition", "freedom"]
    ] = None

    decision_style: Optional[
        Literal["fast", "research", "advice", "emotional"]
    ] = None


# =========================================================
# MASTER REQUEST MODEL
# =========================================================

class LifeSignifyRequest(BaseModel):

    # 🔹 Core Numerology
    identity: BasicIdentity
    birth_details: BirthDetails
    focus: FocusArea

    # 🔹 Personalization
    current_problem: Optional[str] = None

    # 🔹 Optional Contact
    contact: Optional[ContactLayer] = None

    # 🔹 Behavioral Scoring
    financial: Optional[FinancialSnapshot] = None
    career: Optional[CareerProfile] = None
    emotional: Optional[EmotionalState] = None

    # 🔹 Advanced Layers
    life_events: Optional[LifeEvents] = None
    business_history: Optional[BusinessHistory] = None
    health: Optional[HealthLifestyle] = None
    calibration: Optional[CalibrationAnswers] = None

    # 🔹 Internal testing override
    plan_override: Optional[
        Literal["basic", "pro", "premium", "enterprise"]
    ] = None

    model_config = {
        "extra": "ignore"
    }