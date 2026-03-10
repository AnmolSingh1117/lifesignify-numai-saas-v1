export default function StepReview({ submit, prev }: any) {
  return (
    <div>
      <h2 className="text-xl font-semibold mb-6">Review & Generate</h2>

      <div className="flex justify-between">
        <button onClick={prev} className="btn-secondary">
          Back
        </button>

        <button
          onClick={submit}
          className="bg-green-600 hover:bg-green-500 px-6 py-2 rounded-lg"
        >
          Generate Report
        </button>
      </div>
    </div>
  );
}