import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { toast } from "react-hot-toast";
import API from "../../services/api";

import StepIdentity from "../../components/reports/steps/StepIdentity";
import StepBirthDetails from "../../components/reports/steps/StepBirthDetails";
import StepFocus from "../../components/reports/steps/StepFocus";
import StepFinancial from "../../components/reports/steps/StepFinancial";
import StepEmotional from "../../components/reports/steps/StepEmotional";
import StepBusiness from "../../components/reports/steps/StepBusiness";
import StepHealth from "../../components/reports/steps/StepHealth";
import StepCalibration from "../../components/reports/steps/StepCalibration";
import StepReview from "../../components/reports/steps/StepReview";

interface Props {
  user: any;
}

export default function GenerateReportPage({ user }: Props) {
  const navigate = useNavigate();
  const [step, setStep] = useState(1);
  const [submitting, setSubmitting] = useState(false);

  const [formData, setFormData] = useState<any>({
    identity: {},
    birth_details: {},
    focus: {},
    financial: {},
    emotional: {},
    business_history: {},
    health: {},
    calibration: {},
  });

  const plan = user?.subscription?.plan_name?.toLowerCase() || "basic";

  const steps: any[] = [
    { key: "identity", component: StepIdentity },
    { key: "birth_details", component: StepBirthDetails },
    { key: "focus", component: StepFocus },
  ];

  if (plan !== "basic") {
    steps.push(
      { key: "financial", component: StepFinancial },
      { key: "emotional", component: StepEmotional }
    );
  }

  if (plan === "enterprise") {
    steps.push(
      { key: "business_history", component: StepBusiness },
      { key: "health", component: StepHealth },
      { key: "calibration", component: StepCalibration }
    );
  }

  steps.push({ key: "review", component: StepReview });

  const totalSteps = steps.length;
  const CurrentStepComponent = steps[step - 1].component;

  const next = () => step < totalSteps && setStep(step + 1);
  const prev = () => step > 1 && setStep(step - 1);

  // =====================================================
  // VALIDATION + SAFE SUBMIT
  // =====================================================

  const handleSubmit = async () => {
    // Frontend validation
    if (
      !formData.identity?.full_name ||
      !formData.identity?.country_of_residence ||
      !formData.birth_details?.date_of_birth ||
      !formData.birth_details?.birthplace_city ||
      !formData.birth_details?.birthplace_country ||
      !formData.focus?.life_focus
    ) {
      toast.error("Please fill all required fields.");
      return;
    }

    setSubmitting(true);

    try {
      const payload = {
        identity: formData.identity,
        birth_details: formData.birth_details,
        focus: formData.focus,
        financial:
          Object.keys(formData.financial || {}).length > 0
            ? formData.financial
            : undefined,
        emotional:
          Object.keys(formData.emotional || {}).length > 0
            ? formData.emotional
            : undefined,
        business_history:
          Object.keys(formData.business_history || {}).length > 0
            ? formData.business_history
            : undefined,
        health:
          Object.keys(formData.health || {}).length > 0
            ? formData.health
            : undefined,
        calibration:
          Object.keys(formData.calibration || {}).length > 0
            ? formData.calibration
            : undefined,
      };

      console.log("Submitting payload:", payload);

      await API.post("/reports/generate-ai-report", payload);

      toast.success("Report generated successfully 🚀");
      navigate("/dashboard");
    } catch (error: any) {
      console.error("Backend Error:", error?.response?.data);

      if (error?.response?.status === 422) {
        const details = error.response.data?.detail;

        if (Array.isArray(details)) {
          const message = details
            .map((err: any) => `${err.loc?.join(" → ")} : ${err.msg}`)
            .join("\n");

          toast.error(message);
        } else {
          toast.error("Invalid input data.");
        }
      } else if (error?.response?.status === 403) {
        toast.error(
          error?.response?.data?.detail ||
            "Your subscription does not allow this."
        );
      } else {
        toast.error("Something went wrong.");
      }
    } finally {
      setSubmitting(false);
    }
  };

  return (
    <div className="max-w-3xl mx-auto py-10 px-4">
      {/* Progress */}
      <div className="w-full bg-gray-800 h-2 rounded-full mb-6">
        <div
          className="bg-indigo-600 h-2 rounded-full transition-all"
          style={{ width: `${(step / totalSteps) * 100}%` }}
        />
      </div>

      <p className="text-sm text-gray-400 mb-6">
        Step {step} of {totalSteps}
      </p>

      <CurrentStepComponent
        formData={formData}
        setFormData={setFormData}
        next={next}
        prev={prev}
        submit={handleSubmit}
        plan={plan}
        submitting={submitting}
      />
    </div>
  );
}