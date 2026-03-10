import React from "react";

interface Props {
  formData: any;
  setFormData: any;
  next: () => void;
  prev: () => void;
}

export default function StepFocus({
  formData,
  setFormData,
  next,
  prev,
}: Props) {
  const update = (value: string) => {
    setFormData({
      ...formData,
      focus: { life_focus: value },
    });
  };

  return (
    <div className="space-y-6">
      <h2 className="text-xl font-semibold">Primary Focus</h2>

      <select
        className="input"
        onChange={(e) => update(e.target.value)}
      >
        <option value="">Select</option>
        <option value="career_growth">Career Growth</option>
        <option value="business_expansion">Business Expansion</option>
        <option value="relationship">Relationship</option>
        <option value="wealth">Wealth</option>
      </select>

      <div className="flex justify-between">
        <button onClick={prev} className="btn-secondary">Back</button>
        <button onClick={next} className="btn-primary">Continue</button>
      </div>
    </div>
  );
}