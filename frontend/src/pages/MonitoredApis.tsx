import { useState } from "react";
import type { FormEvent } from "react";
import {
  useMonitoredApis,
  useCreateMonitoredApi,
  useDeleteMonitoredApi,
  useToggleMonitoredApi,
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
      {
        name,
        url,
        method,
        expected_status_code: expectedStatus,
        monitoring_interval: interval,
        timeout,
      },
      {
        onSuccess: () => {
          setShowForm(false);
          setName(""); setUrl(""); setMethod("GET");
          setExpectedStatus(200); setInterval_(60); setTimeout_(5);
        },
      }
    );
  };

  if (isLoading) return <p className="p-8">Loading...</p>;
  if (error) return <p className="p-8 text-red-500">Failed to load monitored APIs.</p>;

  return (
    <div className="p-8">
      <div className="flex justify-between items-center mb-6">
        <h2 className="text-xl font-bold">Monitored APIs</h2>
        <button
          onClick={() => setShowForm(!showForm)}
          className="bg-blue-600 text-white px-4 py-2 rounded"
        >
          {showForm ? "Cancel" : "+ Add API"}
        </button>
      </div>

      {showForm && (
        <form onSubmit={handleCreate} className="bg-white p-6 rounded shadow mb-6 grid grid-cols-2 gap-4">
          <input placeholder="Name" value={name} onChange={(e) => setName(e.target.value)} className="border p-2 rounded" required />
          <input placeholder="URL (https://...)" value={url} onChange={(e) => setUrl(e.target.value)} className="border p-2 rounded" required />
          <select value={method} onChange={(e) => setMethod(e.target.value)} className="border p-2 rounded">
            <option>GET</option><option>POST</option><option>PUT</option><option>PATCH</option><option>DELETE</option>
          </select>
          <input type="number" placeholder="Expected Status" value={expectedStatus} onChange={(e) => setExpectedStatus(Number(e.target.value))} className="border p-2 rounded" />
          <input type="number" placeholder="Interval (sec)" value={interval} onChange={(e) => setInterval_(Number(e.target.value))} className="border p-2 rounded" />
          <input type="number" placeholder="Timeout (sec)" value={timeout} onChange={(e) => setTimeout_(Number(e.target.value))} className="border p-2 rounded" />
          <button type="submit" className="col-span-2 bg-green-600 text-white py-2 rounded">
            Create
          </button>
        </form>
      )}

      <div className="bg-white rounded shadow overflow-hidden">
        <table className="w-full text-left">
          <thead className="bg-gray-100">
            <tr>
              <th className="p-3">Name</th>
              <th className="p-3">URL</th>
              <th className="p-3">Method</th>
              <th className="p-3">Interval</th>
              <th className="p-3">Status</th>
              <th className="p-3">Actions</th>
            </tr>
          </thead>
          <tbody>
            {apis?.map((api) => (
              <tr key={api.id} className="border-t">
                <td className="p-3">{api.name}</td>
                <td className="p-3 text-sm text-gray-600">{api.url}</td>
                <td className="p-3">{api.method}</td>
                <td className="p-3">{api.monitoring_interval}s</td>
                <td className="p-3">
                  <span className={`px-2 py-1 rounded text-xs ${api.active ? "bg-green-100 text-green-700" : "bg-gray-200 text-gray-600"}`}>
                    {api.active ? "Active" : "Paused"}
                  </span>
                </td>
                <td className="p-3 space-x-2">
                  <button
                    onClick={() => toggleMutation.mutate({ id: api.id, enable: !api.active })}
                    className="text-blue-600 text-sm"
                  >
                    {api.active ? "Disable" : "Enable"}
                  </button>
                  <button
                    onClick={() => { if (confirm("Delete this API?")) deleteMutation.mutate(api.id); }}
                    className="text-red-600 text-sm"
                  >
                    Delete
                  </button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
        {apis?.length === 0 && <p className="p-4 text-gray-500">No monitored APIs yet.</p>}
      </div>
    </div>
  );
}