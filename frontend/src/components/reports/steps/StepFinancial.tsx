import React from "react";

interface Props {
  formData: any;
  setFormData: any;
  next: () => void;
  prev: () => void;
}

export default function StepFinancial({
  formData,
  setFormData,
  next,
  prev,
}: Props) {
  const update = (value: string) => {
    setFormData({
      ...formData,
      financial: { income_level: value },
    });
  };

  return (
    <div className="space-y-6">
      <h2 className="text-xl font-semibold">Financial Snapshot</h2>

      <input
        placeholder="Monthly Income"
        className="input"
        onChange={(e) => update(e.target.value)}
      />

      <div className="flex justify-between">
        <button onClick={prev} className="btn-secondary">Back</button>
        <button onClick={next} className="btn-primary">Continue</button>
      </div>
    </div>
  );
}