import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import API from "../../services/api";

import {
  Radar,
  RadarChart,
  PolarGrid,
  PolarAngleAxis,
  PolarRadiusAxis,
  ResponsiveContainer,
} from "recharts";

export default function DashboardPage() {
  const [report, setReport] = useState<any>(null);
  const [reports, setReports] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);
  const navigate = useNavigate();

  /* ===============================
     FETCH REPORTS (SAFE)
  ================================= */
  const fetchReports = async () => {
    try {
      const res = await API.get("/reports/");
      setReports(res.data);

      if (res.data.length > 0) {
        setReport(res.data[res.data.length - 1]);
      }
    } catch (err: any) {
      if (err.response?.status === 401) {
        localStorage.removeItem("access_token");
        navigate("/login");
      }
      console.error("Fetch Reports Error:", err);
    } finally {
      setLoading(false);
    }
  };

  /* ===============================
     INITIAL LOAD (SAFE)
  ================================= */
  useEffect(() => {
    const token = localStorage.getItem("access_token");

    if (!token) {
      navigate("/login");
      return;
    }

    fetchReports();
  }, []);

  /* ===============================
     GENERATE REPORT
  ================================= */
  const generateReport = async () => {
    try {
      await API.post("/reports/generate-ai-report", {
        financial: {},
        career: {},
        emotional: {},
        focus: {},
        life_events: {},
      });

      fetchReports();
    } catch (err: any) {
      if (err.response?.status === 403) {
        navigate("/upgrade");
      }
      if (err.response?.status === 401) {
        navigate("/login");
      }
    }
  };

  /* ===============================
     DOWNLOAD PDF
  ================================= */
  const downloadPDF = async () => {
    if (!report) return;

    try {
      const response = await API.get(
        `/reports/${report.id}/download-pdf`,
        { responseType: "blob" }
      );

      const blob = new Blob([response.data], {
        type: "application/pdf",
      });

      const url = window.URL.createObjectURL(blob);
      const link = document.createElement("a");
      link.href = url;
      link.download = "LifeSignifyReport.pdf";
      link.click();
    } catch (err: any) {
      if (err.response?.status === 403) {
        navigate("/upgrade");
      }
      if (err.response?.status === 401) {
        navigate("/login");
      }
    }
  };

  /* ===============================
     LOADING STATE
  ================================= */
  if (loading) {
    return (
      <div className="text-gray-400 text-center mt-20">
        Loading Dashboard...
      </div>
    );
  }

  /* ===============================
     EMPTY STATE
  ================================= */
  if (!report) {
    return (
      <div className="text-gray-400 text-center mt-20">
        No reports yet
        <div className="mt-6">
          <button
            onClick={generateReport}
            className="bg-indigo-600 hover:bg-indigo-700 px-6 py-2 rounded-xl"
          >
            Generate First Report
          </button>
        </div>
      </div>
    );
  }

  const dashboard = report.content?.executive_dashboard;

  const radarData = [
    { subject: "Life Stability", value: dashboard?.life_stability_index || 0 },
    { subject: "Financial", value: dashboard?.financial_discipline_index || 0 },
    { subject: "Clarity", value: dashboard?.decision_clarity_score || 0 },
    { subject: "Emotional", value: dashboard?.emotional_regulation_index || 0 },
    { subject: "Dharma", value: dashboard?.dharma_alignment_score || 0 },
  ];

  return (
    <div className="min-h-screen bg-black text-white p-10 space-y-10">

      <h1 className="text-3xl font-bold text-indigo-400">
        Life Signify Intelligence Dashboard
      </h1>

      {/* Buttons */}
      <div className="flex gap-4">
        <button
          onClick={generateReport}
          className="bg-indigo-600 hover:bg-indigo-700 px-6 py-2 rounded-xl"
        >
          Generate AI Report
        </button>

        <button
          onClick={downloadPDF}
          className="bg-emerald-600 hover:bg-emerald-700 px-6 py-2 rounded-xl"
        >
          Download PDF
        </button>
      </div>

      {/* KPI Cards */}
      <div className="grid grid-cols-3 gap-6">
        <Card title="Life Stability" value={dashboard?.life_stability_index} />
        <Card title="Financial Discipline" value={dashboard?.financial_discipline_index} />
        <Card title="Dharma Alignment" value={dashboard?.dharma_alignment_score} />
      </div>

      {/* Radar Chart */}
      <div className="bg-white/5 p-8 rounded-2xl border border-white/10">
        <h3 className="text-xl text-indigo-300 mb-4 font-semibold">
          Performance Radar
        </h3>

        <ResponsiveContainer width="100%" height={400}>
          <RadarChart data={radarData}>
            <PolarGrid />
            <PolarAngleAxis dataKey="subject" />
            <PolarRadiusAxis domain={[0, 100]} />
            <Radar
              name="Score"
              dataKey="value"
              stroke="#6366f1"
              fill="#6366f1"
              fillOpacity={0.6}
            />
          </RadarChart>
        </ResponsiveContainer>
      </div>

      {/* AI Narrative */}
      <div className="bg-white/5 p-8 rounded-2xl border border-white/10">
        <h3 className="text-xl text-indigo-300 mb-4 font-semibold">
          AI Narrative Insight
        </h3>
        <p className="text-gray-300 whitespace-pre-line">
          {report.content?.ai_narrative?.ai_full_narrative}
        </p>
      </div>

      {/* Report History */}
      <div className="bg-white/5 p-8 rounded-2xl border border-white/10">
        <h3 className="text-xl text-indigo-300 mb-4 font-semibold">
          Report History
        </h3>

        <table className="w-full text-left text-gray-300">
          <thead>
            <tr className="border-b border-gray-700">
              <th className="py-2">Date</th>
              <th className="py-2">Engine</th>
              <th className="py-2">Score</th>
            </tr>
          </thead>
          <tbody>
            {reports.map((r) => (
              <tr key={r.id} className="border-b border-gray-800">
                <td className="py-2">
                  {new Date(r.created_at).toLocaleDateString()}
                </td>
                <td>{r.engine_version}</td>
                <td>
                  {r.content?.executive_dashboard?.life_stability_index}
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}

function Card({ title, value }: any) {
  return (
    <div className="bg-[#1e293b] p-6 rounded-xl border border-white/10">
      <h3 className="text-sm text-gray-400">{title}</h3>
      <p className="text-3xl font-bold mt-2 text-emerald-400">
        {value ?? "--"}
      </p>
    </div>
  );
}
