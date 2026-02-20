import { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import API from "../../services/api";
import toast from "react-hot-toast";

interface Report {
  id: number;
  title?: string;
  created_at: string;
  status?: string;
}

export default function ReportsListPage() {
  const [reports, setReports] = useState<Report[]>([]);
  const [loading, setLoading] = useState(true);
  const [generating, setGenerating] = useState(false);
  const [error, setError] = useState("");

  const fetchReports = async () => {
    try {
      const res = await API.get("/reports/");
      setReports(res.data);
    } catch {
      setError("Failed to load reports.");
      toast.error("Failed to load reports");
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchReports();
  }, []);

  const generateReport = async () => {
    const loadingToast = toast.loading("Generating AI Report...");
    setGenerating(true);

    try {
      await API.post("/reports/generate-ai-report", {
        identity: {
          full_name: "Jay Prakash",
          date_of_birth: "20/02/1990",
          gender: "male",
          country_of_residence: "India",
        },
        birth_details: {
          date_of_birth: "20/02/1990",
          time_of_birth: "10:30 AM",
          birthplace_city: "Mumbai",
          birthplace_country: "India",
        },
        focus: {
          life_focus: "career_growth",
        },
      });

      toast.success("AI Report generated successfully 🚀", {
        id: loadingToast,
      });

      fetchReports();
    } catch (error: any) {
      toast.error(
        error?.response?.data?.detail || "Failed to generate report",
        { id: loadingToast }
      );
    } finally {
      setGenerating(false);
    }
  };

  if (loading) {
    return (
      <div className="min-h-screen bg-gray-950 text-white flex items-center justify-center">
        <div className="animate-pulse text-lg">Loading Reports...</div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="min-h-screen bg-gray-950 text-red-400 flex items-center justify-center">
        {error}
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-950 text-white p-8">

      <div className="flex justify-between items-center mb-8">
        <h1 className="text-3xl font-bold">My Reports</h1>

        <button
          onClick={generateReport}
          disabled={generating}
          className="bg-indigo-600 hover:bg-indigo-500 px-5 py-2 rounded-lg transition disabled:opacity-50"
        >
          {generating ? "Generating..." : "Generate New Report"}
        </button>
      </div>

      {reports.length === 0 ? (
        <div className="bg-gray-900 p-8 rounded-xl text-center text-gray-400">
          No reports found. Generate your first AI insight report.
        </div>
      ) : (
        <div className="space-y-5">
          {reports.map((report) => (
            <div
              key={report.id}
              className="bg-gray-900 p-6 rounded-xl flex justify-between items-center hover:bg-gray-800 transition"
            >
              <div>
                <p className="text-lg font-semibold">
                  {report.title || `Report #${report.id}`}
                </p>
                <p className="text-sm text-gray-400">
                  Created: {new Date(report.created_at).toLocaleString()}
                </p>
                {report.status && (
                  <p className="text-xs text-indigo-400 mt-1">
                    Status: {report.status}
                  </p>
                )}
              </div>

              <Link
                to={`/reports/${report.id}`}
                className="bg-indigo-600 hover:bg-indigo-500 px-4 py-2 rounded-lg transition"
              >
                View
              </Link>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}