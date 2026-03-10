export default function StepBusiness({ next, prev }: any) {
  return (
    <div>
      <h2 className="text-xl font-semibold mb-6">Business History</h2>
      <div className="flex justify-between">
        <button onClick={prev} className="btn-secondary">Back</button>
        <button onClick={next} className="btn-primary">Continue</button>
      </div>
    </div>
  );
}