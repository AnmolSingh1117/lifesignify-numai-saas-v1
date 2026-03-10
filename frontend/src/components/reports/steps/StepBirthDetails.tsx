import React from "react";

interface Props {
  formData: any;
  setFormData: any;
  next: () => void;
  prev: () => void;
}

export default function StepBirthDetails({
  formData,
  setFormData,
  next,
  prev,
}: Props) {
  const update = (field: string, value: string) => {
    setFormData({
      ...formData,
      birth_details: {
        ...formData.birth_details,
        [field]: value,
      },
    });
  };

  return (
    <div className="space-y-6">
      <h2 className="text-xl font-semibold">Birth Details</h2>

      <input
        type="date"
        className="input"
        onChange={(e) => update("date_of_birth", e.target.value)}
      />

      <input
        placeholder="Time of Birth"
        className="input"
        onChange={(e) => update("time_of_birth", e.target.value)}
      />

      <input
        placeholder="Birth City"
        className="input"
        onChange={(e) => update("birthplace_city", e.target.value)}
      />

      <div className="flex justify-between">
        <button onClick={prev} className="btn-secondary">
          Back
        </button>
        <button onClick={next} className="btn-primary">
          Continue
        </button>
      </div>
    </div>
  );
}