import { useParams, Link } from "react-router-dom";
import { LineChart, Line, XAxis, YAxis, Tooltip, ResponsiveContainer } from "recharts";
import { useMetrics, useChecks } from "../hooks/useMetrics";

export default function ApiDetail() {
  const { id } = useParams();
  const apiId = Number(id);
  const { data: metrics } = useMetrics(apiId);
  const { data: checks } = useChecks(apiId);

  const chartData = checks
    ?.slice()
    .reverse()
    .map((c) => ({
      time: new Date(c.checked_at).toLocaleTimeString(),
      responseTime: c.response_time ?? 0,
    }));

  return (
    <div className="p-8">
      <Link to="/dashboard" className="text-blue-600 text-sm">&larr; Back</Link>
      <h2 className="text-xl font-bold my-4">API #{apiId} Metrics</h2>

      {metrics && (
        <div className="grid grid-cols-4 gap-4 mb-6">
          <div className="bg-white p-4 rounded shadow">
            <p className="text-sm text-gray-500">Uptime</p>
            <p className="text-2xl font-bold">{metrics.uptime_percentage}%</p>
          </div>
          <div className="bg-white p-4 rounded shadow">
            <p className="text-sm text-gray-500">Error Rate</p>
            <p className="text-2xl font-bold">{metrics.error_rate}%</p>
          </div>
          <div className="bg-white p-4 rounded shadow">
            <p className="text-sm text-gray-500">Avg Response</p>
            <p className="text-2xl font-bold">{metrics.average_response_time ?? "-"}ms</p>
          </div>
          <div className="bg-white p-4 rounded shadow">
            <p className="text-sm text-gray-500">Total Checks</p>
            <p className="text-2xl font-bold">{metrics.total_checks}</p>
          </div>
        </div>
      )}

      <div className="bg-white p-4 rounded shadow">
        <h3 className="font-semibold mb-2">Response Time (ms)</h3>
        <ResponsiveContainer width="100%" height={300}>
          <LineChart data={chartData}>
            <XAxis dataKey="time" tick={{ fontSize: 10 }} />
            <YAxis />
            <Tooltip />
            <Line type="monotone" dataKey="responseTime" stroke="#2563eb" dot={false} />
          </LineChart>
        </ResponsiveContainer>
      </div>
    </div>
  );
}