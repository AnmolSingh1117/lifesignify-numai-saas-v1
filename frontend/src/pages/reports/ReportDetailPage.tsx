import { useEffect, useState } from "react";
import { useParams, Link } from "react-router-dom";
import API from "../../services/api";
import RadarChartComponent from "../../components/dashboard/RadarChartComponent";
import { useAuth } from "../../context/AuthContext";
import toast from "react-hot-toast";

interface ExecutiveDashboard {
  life_stability_index?: number;
  financial_discipline_index?: number;
  emotional_regulation_index?: number;
  dharma_alignment_score?: number;
  karma_pressure_index?: number;
}

interface AINarrative {
  executive_summary?: string;
  psychological_pattern?: string;
  strategic_advice?: string;
  plan_30_day?: string;
  plan_90_day?: string;
}

interface Report {
  id: number;
  title?: string;
  created_at: string;
  executive_dashboard?: ExecutiveDashboard;
  radar_chart_data?: any;
  ai_narrative?: AINarrative;
  risk_analysis?: string;
  remedy_direction?: string;
  status?: string;
}

export default function ReportDetailPage() {
  const { id } = useParams<{ id: string }>();
  const { user } = useAuth();

  const [report, setReport] = useState<Report | null>(null);
  const [loading, setLoading] = useState(true);
  const [generating, setGenerating] = useState(false);
  const [error, setError] = useState("");

  const isPro = user?.plan === "pro";

  useEffect(() => {
    if (!id) return;

    const fetchReport = async () => {
      try {
        const res = await API.get(`/reports/${id}`);
        setReport(res.data);
      } catch {
        setError("Failed to load report.");
        toast.error("Failed to load report");
      } finally {
        setLoading(false);
      }
    };

    fetchReport();
  }, [id]);

  // ✅ FIXED GENERATE FUNCTION
  const generateNewReport = async () => {
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

      toast.success("New AI Report generated 🚀", {
        id: loadingToast,
      });

      window.location.href = "/reports";
    } catch (error: any) {
      toast.error(
        error?.response?.data?.detail || "Failed to generate report",
        { id: loadingToast }
      );
    } finally {
      setGenerating(false);
    }
  };

  const downloadPDF = async () => {
    if (!id) return;

    const loadingToast = toast.loading("Preparing PDF...");

    try {
      const response = await API.get(`/reports/${id}/export-pdf`, {
        responseType: "blob",
      });

      const url = window.URL.createObjectURL(new Blob([response.data]));
      const link = document.createElement("a");
      link.href = url;
      link.setAttribute("download", `report-${id}.pdf`);
      document.body.appendChild(link);
      link.click();

      toast.success("Report downloaded successfully", {
        id: loadingToast,
      });
    } catch {
      toast.error("Failed to download PDF", {
        id: loadingToast,
      });
    }
  };

  if (loading) {
    return (
      <div className="min-h-screen bg-gray-950 text-white flex items-center justify-center">
        <div className="animate-pulse text-lg">Loading Report...</div>
      </div>
    );
  }

  if (error || !report) {
    return (
      <div className="min-h-screen bg-gray-950 text-red-400 flex items-center justify-center">
        {error || "Report not found."}
      </div>
    );
  }

  const dashboard = report.executive_dashboard;
  const ai = report.ai_narrative;

  const radarData =
    report.radar_chart_data ??
    (dashboard
      ? [
          { metric: "Life Stability", score: dashboard.life_stability_index ?? 0 },
          { metric: "Financial Discipline", score: dashboard.financial_discipline_index ?? 0 },
          { metric: "Emotional Regulation", score: dashboard.emotional_regulation_index ?? 0 },
          { metric: "Dharma Alignment", score: dashboard.dharma_alignment_score ?? 0 },
          { metric: "Karma Pressure", score: dashboard.karma_pressure_index ?? 0 },
        ]
      : []);

  return (
    <div className="min-h-screen bg-gray-950 text-white p-8 space-y-10">

      {/* Header */}
      <div className="flex justify-between items-center">
        <div>
          <h1 className="text-3xl font-bold">
            {report.title || "Life Intelligence Report"}
          </h1>
          <p className="text-gray-400 text-sm">
            Created: {new Date(report.created_at).toLocaleString()}
          </p>
        </div>

        <div className="flex gap-4">
          <button
            onClick={generateNewReport}
            disabled={generating}
            className="bg-emerald-600 hover:bg-emerald-500 px-5 py-2 rounded-lg transition disabled:opacity-50"
          >
            {generating ? "Generating..." : "Generate New Report"}
          </button>

          <button
            onClick={downloadPDF}
            className="bg-indigo-600 hover:bg-indigo-500 transition px-5 py-2 rounded-lg"
          >
            Download PDF
          </button>
        </div>
      </div>

      {dashboard && (
        <div>
          <h2 className="text-xl font-semibold mb-6">
            Executive Dashboard
          </h2>

          <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
            <ScoreCard label="Life Stability" value={dashboard.life_stability_index} />
            <ScoreCard label="Financial Discipline" value={dashboard.financial_discipline_index} />
            <ScoreCard label="Emotional Regulation" value={dashboard.emotional_regulation_index} />
            <ScoreCard label="Dharma Alignment" value={dashboard.dharma_alignment_score} />
            <ScoreCard label="Karma Pressure" value={dashboard.karma_pressure_index} />
          </div>
        </div>
      )}

      {radarData.length > 0 && (
        <RadarChartComponent data={radarData} />
      )}

      {ai && (
        <div className="space-y-6">
          <h2 className="text-xl font-semibold">AI Strategic Analysis</h2>

          {ai.executive_summary && (
            <Section title="Executive Summary" content={ai.executive_summary} />
          )}

          {ai.psychological_pattern && (
            <Section title="Psychological Pattern" content={ai.psychological_pattern} />
          )}

          {ai.strategic_advice && (
            <Section title="Strategic Advice" content={ai.strategic_advice} />
          )}

          {ai.plan_30_day && (
            <Section title="30 Day Plan" content={ai.plan_30_day} />
          )}

          {ai.plan_90_day && (
            <Section title="90 Day Plan" content={ai.plan_90_day} />
          )}
        </div>
      )}

      {report.risk_analysis && (
        <Section title="Risk Analysis" content={report.risk_analysis} />
      )}

      {report.remedy_direction && (
        <Section title="Remedy Direction" content={report.remedy_direction} />
      )}
    </div>
  );
}

function ScoreCard({ label, value }: { label: string; value?: number }) {
  return (
    <div className="bg-gray-900 p-6 rounded-xl shadow-md">
      <p className="text-sm text-gray-400">{label}</p>
      <p className="text-3xl font-bold mt-2">
        {value ?? "--"}
      </p>
    </div>
  );
}

function Section({ title, content }: { title: string; content: string }) {
  return (
    <div className="bg-gray-900 p-6 rounded-xl">
      <h2 className="text-xl font-semibold mb-3">{title}</h2>
      <p className="text-gray-300 whitespace-pre-line">{content}</p>
    </div>
  );
}