import React from "react";

interface Props {
  formData: any;
  setFormData: any;
  next: () => void;
}

export default function StepIdentity({ formData, setFormData, next }: Props) {
  const update = (field: string, value: string) => {
    setFormData({
      ...formData,
      identity: {
        ...formData.identity,
        [field]: value,
      },
    });
  };

  return (
    <div className="space-y-6">
      <h2 className="text-xl font-semibold">Identity Details</h2>

      <input
        placeholder="Full Name"
        className="input"
        onChange={(e) => update("full_name", e.target.value)}
      />

      <input
        placeholder="Gender"
        className="input"
        onChange={(e) => update("gender", e.target.value)}
      />

      <input
        placeholder="Country"
        className="input"
        onChange={(e) => update("country_of_residence", e.target.value)}
      />

      <button onClick={next} className="btn-primary">
        Continue
      </button>
    </div>
  );
}