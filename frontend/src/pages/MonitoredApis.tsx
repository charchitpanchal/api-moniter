import { useState } from "react";
import type { FormEvent } from "react";
import { Link } from "react-router-dom";
import {
  useMonitoredApis, useCreateMonitoredApi, useDeleteMonitoredApi, useToggleMonitoredApi,
} from "../hooks/useMonitoredApis";

export default function MonitoredApis() {
  const { data: apis, isLoading, error } = useMonitoredApis();
  const createMutation = useCreateMonitoredApi();
  const deleteMutation = useDeleteMonitoredApi();
  const toggleMutation = useToggleMonitoredApi();
  const [showForm, setShowForm] = useState(false);
  const [name, setName] = useState("");
  const [url, setUrl] = useState("");
  const [method, setMethod] = useState("GET");
  const [expectedStatus, setExpectedStatus] = useState(200);
  const [interval, setInterval_] = useState(60);
  const [timeout, setTimeout_] = useState(5);

  const handleCreate = (e: FormEvent) => {
    e.preventDefault();
    createMutation.mutate(
      { name, url, method, expected_status_code: expectedStatus, monitoring_interval: interval, timeout },
      { onSuccess: () => { setShowForm(false); setName(""); setUrl(""); setMethod("GET"); setExpectedStatus(200); setInterval_(60); setTimeout_(5); } }
    );
  };

  if (isLoading) return <div className="max-w-6xl mx-auto p-8"><p className="text-slate-500">Loading...</p></div>;
  if (error) return <div className="max-w-6xl mx-auto p-8"><p className="text-red-500">Failed to load monitored APIs.</p></div>;

  return (
    <div className="max-w-6xl mx-auto p-8">
      <div className="flex justify-between items-center mb-6">
        <div>
          <h2 className="text-2xl font-bold text-slate-800">Monitored APIs</h2>
          <p className="text-slate-500 text-sm mt-1">{apis?.length ?? 0} API{apis?.length === 1 ? "" : "s"} tracked</p>
        </div>
        <button onClick={() => setShowForm(!showForm)}
          className="bg-indigo-600 hover:bg-indigo-700 text-white px-5 py-2.5 rounded-lg font-medium shadow-sm transition">
          {showForm ? "Cancel" : "+ Add API"}
        </button>
      </div>

      {showForm && (
        <form onSubmit={handleCreate} className="bg-white p-6 rounded-xl shadow-sm border border-slate-200 mb-6 grid grid-cols-2 gap-4">
          <input placeholder="Name" value={name} onChange={(e) => setName(e.target.value)} className="border border-slate-300 p-2.5 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 outline-none" required />
          <input placeholder="URL (https://...)" value={url} onChange={(e) => setUrl(e.target.value)} className="border border-slate-300 p-2.5 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 outline-none" required />
          <select value={method} onChange={(e) => setMethod(e.target.value)} className="border border-slate-300 p-2.5 rounded-lg">
            <option>GET</option><option>POST</option><option>PUT</option><option>PATCH</option><option>DELETE</option>
          </select>
          <input type="number" placeholder="Expected Status" value={expectedStatus} onChange={(e) => setExpectedStatus(Number(e.target.value))} className="border border-slate-300 p-2.5 rounded-lg" />
          <input type="number" placeholder="Interval (sec)" value={interval} onChange={(e) => setInterval_(Number(e.target.value))} className="border border-slate-300 p-2.5 rounded-lg" />
          <input type="number" placeholder="Timeout (sec)" value={timeout} onChange={(e) => setTimeout_(Number(e.target.value))} className="border border-slate-300 p-2.5 rounded-lg" />
          <button type="submit" className="col-span-2 bg-emerald-600 hover:bg-emerald-700 text-white py-2.5 rounded-lg font-medium transition">Create</button>
        </form>
      )}

      <div className="bg-white rounded-xl shadow-sm border border-slate-200 overflow-hidden">
        <table className="w-full text-left">
          <thead className="bg-slate-50 border-b border-slate-200">
            <tr className="text-slate-500 text-xs uppercase tracking-wide">
              <th className="p-4">Name</th><th className="p-4">URL</th><th className="p-4">Method</th>
              <th className="p-4">Interval</th><th className="p-4">Status</th><th className="p-4">Actions</th>
            </tr>
          </thead>
          <tbody>
            {apis?.map((api) => (
              <tr key={api.id} className="border-t border-slate-100 hover:bg-slate-50 transition">
                <td className="p-4"><Link to={`/apis/${api.id}`} className="text-indigo-600 font-medium hover:underline">{api.name}</Link></td>
                <td className="p-4 text-sm text-slate-500 truncate max-w-xs">{api.url}</td>
                <td className="p-4"><span className="text-xs font-mono bg-slate-100 px-2 py-1 rounded">{api.method}</span></td>
                <td className="p-4 text-slate-600">{api.monitoring_interval}s</td>
                <td className="p-4">
                  <span className={`px-2.5 py-1 rounded-full text-xs font-medium ${api.active ? "bg-emerald-100 text-emerald-700" : "bg-slate-200 text-slate-600"}`}>
                    {api.active ? "● Active" : "○ Paused"}
                  </span>
                </td>
                <td className="p-4 space-x-3">
                  <button onClick={() => toggleMutation.mutate({ id: api.id, enable: !api.active })} className="text-indigo-600 text-sm font-medium hover:underline">
                    {api.active ? "Disable" : "Enable"}
                  </button>
                  <button onClick={() => { if (confirm("Delete this API?")) deleteMutation.mutate(api.id); }} className="text-red-500 text-sm font-medium hover:underline">
                    Delete
                  </button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
        {apis?.length === 0 && <p className="p-8 text-center text-slate-400">No monitored APIs yet. Click "+ Add API" to get started.</p>}
      </div>
    </div>
  );
}