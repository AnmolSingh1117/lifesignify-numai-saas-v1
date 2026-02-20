import { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import API from "../../services/api";
import { useAuth } from "../../context/AuthContext";
import toast from "react-hot-toast";

interface Report {
  id: number;
  created_at: string;
  executive_dashboard?: {
    life_stability_index?: number;
  };
  risk_analysis?: string;
}

export default function DashboardPage() {
  const { user } = useAuth();
  const [reports, setReports] = useState<Report[]>([]);
  const [loading, setLoading] = useState(true);
  const [generating, setGenerating] = useState(false);

  const fetchReports = async () => {
    try {
      const res = await API.get("/reports/");
      setReports(res.data);
    } catch {
      toast.error("Failed to fetch reports");
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchReports();
  }, []);

  const handleGenerateReport = async () => {
    if (generating) return;

    setGenerating(true);
    const loadingToast = toast.loading("Generating AI report...");

    try {
      await API.post("/reports/generate-ai-report", {
        identity: {
          full_name: user?.email || "Test User",
          date_of_birth: "01/01/1990", // DD/MM/YYYY REQUIRED
          gender: "male",
          country_of_residence: "India"
        },
        birth_details: {
          date_of_birth: "01/01/1990",
          time_of_birth: "10:30 AM", // MUST include AM/PM
          birthplace_city: "Mumbai",
          birthplace_country: "India"
        },
        focus: {
          life_focus: "general_alignment"
        }
      });

      toast.success("Report generated successfully 🚀", {
        id: loadingToast
      });

      await fetchReports();
    } catch (error: any) {
      toast.error(
        error?.response?.data?.detail || "Report generation failed",
        { id: loadingToast }
      );
    } finally {
      setGenerating(false);
    }
  };

  const latestReport = reports[0];

  return (
    <div className="min-h-screen bg-gray-950 text-white p-8 space-y-10">

      {/* Header */}
      <div className="flex justify-between items-center">
        <div>
          <h1 className="text-3xl font-bold">
            Welcome, {user?.email}
          </h1>
          <p className="text-gray-400 mt-1">
            Your Life Intelligence Dashboard
          </p>
        </div>

        <PlanBadge isPro={user?.plan === "pro"} />
      </div>

      {/* Metrics */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">

        <MetricCard
          label="Total Reports"
          value={loading ? "..." : reports.length}
        />

        <MetricCard
          label="Latest Stability Score"
          value={
            latestReport?.executive_dashboard?.life_stability_index ?? "--"
          }
        />

        <MetricCard
          label="Latest Risk"
          value={latestReport?.risk_analysis ?? "--"}
        />
      </div>

      {/* Actions */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">

        <button
          onClick={handleGenerateReport}
          disabled={generating}
          className="bg-indigo-600 hover:bg-indigo-500 p-6 rounded-xl font-semibold transition disabled:opacity-50"
        >
          {generating ? "Generating..." : "Generate AI Report"}
        </button>

        <Link
          to="/reports"
          className="bg-indigo-600 hover:bg-indigo-500 p-6 rounded-xl font-semibold text-center"
        >
          View All Reports
        </Link>

        {user?.plan !== "pro" && (
          <Link
            to="/upgrade"
            className="bg-emerald-600 hover:bg-emerald-500 p-6 rounded-xl font-semibold text-center"
          >
            Upgrade to Pro
          </Link>
        )}
      </div>
    </div>
  );
}

function MetricCard({ label, value }: { label: string; value: any }) {
  return (
    <div className="bg-gray-900 p-6 rounded-xl shadow-md">
      <p className="text-sm text-gray-400">{label}</p>
      <p className="text-3xl font-bold mt-2">{value}</p>
    </div>
  );
}

function PlanBadge({ isPro }: { isPro?: boolean }) {
  return (
    <div
      className={`px-4 py-2 rounded-full text-sm font-semibold ${
        isPro ? "bg-emerald-600" : "bg-gray-700"
      }`}
    >
      {isPro ? "PRO PLAN" : "FREE PLAN"}
    </div>
  );
}