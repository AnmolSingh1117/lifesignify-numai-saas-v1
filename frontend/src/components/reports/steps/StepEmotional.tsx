import React from "react";

interface Props {
  formData: any;
  setFormData: any;
  next: () => void;
  prev: () => void;
}

export default function StepEmotional({
  formData,
  setFormData,
  next,
  prev,
}: Props) {
  const update = (value: string) => {
    setFormData({
      ...formData,
      emotional: { stress_level: value },
    });
  };

  return (
    <div className="space-y-6">
      <h2 className="text-xl font-semibold">Emotional State</h2>

      <input
        placeholder="Current Stress Level (1-10)"
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