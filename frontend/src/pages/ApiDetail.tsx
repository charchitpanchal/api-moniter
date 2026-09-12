import { useParams, Link } from "react-router-dom";
import { LineChart, Line, XAxis, YAxis, Tooltip, ResponsiveContainer, CartesianGrid } from "recharts";
import { useMetrics, useChecks } from "../hooks/useMetrics";
import Navbar from "../components/Navbar";

export default function ApiDetail() {
  const { id } = useParams();
  const apiId = Number(id);
  const { data: metrics } = useMetrics(apiId);
  const { data: checks } = useChecks(apiId);

  const chartData = checks?.slice().reverse().map((c) => ({
    time: new Date(c.checked_at).toLocaleTimeString(),
    responseTime: c.response_time ?? 0,
  }));

  return (
    <div className="min-h-screen bg-slate-50">
      <Navbar />
      <div className="max-w-6xl mx-auto p-8">
        <Link to="/dashboard" className="text-indigo-600 text-sm font-medium hover:underline">&larr; Back to Dashboard</Link>
        <h2 className="text-2xl font-bold text-slate-800 my-4">API #{apiId} Metrics</h2>

        {metrics && (
          <div className="grid grid-cols-4 gap-4 mb-6">
            {[
              { label: "Uptime", value: `${metrics.uptime_percentage}%`, color: "text-emerald-600" },
              { label: "Error Rate", value: `${metrics.error_rate}%`, color: "text-red-500" },
              { label: "Avg Response", value: `${metrics.average_response_time ?? "-"}ms`, color: "text-indigo-600" },
              { label: "Total Checks", value: metrics.total_checks, color: "text-slate-700" },
            ].map((card) => (
              <div key={card.label} className="bg-white p-5 rounded-xl shadow-sm border border-slate-200">
                <p className="text-sm text-slate-500">{card.label}</p>
                <p className={`text-3xl font-bold mt-1 ${card.color}`}>{card.value}</p>
              </div>
            ))}
          </div>
        )}

        <div className="bg-white p-6 rounded-xl shadow-sm border border-slate-200">
          <h3 className="font-semibold text-slate-700 mb-4">Response Time (ms)</h3>
          <ResponsiveContainer width="100%" height={300}>
            <LineChart data={chartData}>
              <CartesianGrid strokeDasharray="3 3" stroke="#f1f5f9" />
              <XAxis dataKey="time" tick={{ fontSize: 10, fill: "#94a3b8" }} />
              <YAxis tick={{ fontSize: 11, fill: "#94a3b8" }} />
              <Tooltip contentStyle={{ borderRadius: 8, border: "1px solid #e2e8f0" }} />
              <Line type="monotone" dataKey="responseTime" stroke="#4f46e5" strokeWidth={2} dot={false} />
            </LineChart>
          </ResponsiveContainer>
        </div>
      </div>
    </div>
  );
}