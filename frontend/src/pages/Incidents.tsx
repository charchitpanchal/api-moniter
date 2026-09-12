import { useState } from "react";
import { useIncidents, useAnalyzeIncident } from "../hooks/useIncidents";
import type { AiAnalysis } from "../api/incidents";

const severityColor: Record<string, string> = {
  LOW: "bg-gray-200 text-gray-700",
  MEDIUM: "bg-yellow-100 text-yellow-700",
  HIGH: "bg-orange-100 text-orange-700",
  CRITICAL: "bg-red-100 text-red-700",
};

export default function Incidents() {
  const { data: incidents, isLoading } = useIncidents();
  const analyzeMutation = useAnalyzeIncident();
  const [analysis, setAnalysis] = useState<Record<number, AiAnalysis>>({});
  const [openId, setOpenId] = useState<number | null>(null);

  const handleAnalyze = (id: number) => {
    setOpenId(id);
    analyzeMutation.mutate(id, {
      onSuccess: (data) => setAnalysis((prev) => ({ ...prev, [id]: data })),
    });
  };

  if (isLoading) return <p className="p-8">Loading...</p>;

  return (
    <div className="p-8">
      <h2 className="text-xl font-bold mb-6">Incidents</h2>
      <div className="space-y-4">
        {incidents?.map((inc) => (
          <div key={inc.id} className="bg-white rounded shadow p-4">
            <div className="flex justify-between items-center">
              <div>
                <span className={`px-2 py-1 rounded text-xs font-medium ${severityColor[inc.severity]}`}>
                  {inc.severity}
                </span>
                <span className="ml-3 font-medium">API #{inc.api_id}</span>
                <span className="ml-3 text-sm text-gray-500">{inc.status}</span>
              </div>
              <button
                onClick={() => handleAnalyze(inc.id)}
                className="bg-purple-600 text-white text-sm px-3 py-1 rounded"
                disabled={analyzeMutation.isPending && openId === inc.id}
              >
                {analyzeMutation.isPending && openId === inc.id ? "Analyzing..." : "AI Analyze"}
              </button>
            </div>
            <p className="text-sm text-gray-600 mt-2">{inc.last_error}</p>

            {openId === inc.id && analysis[inc.id] && (
              <div className="mt-4 border-t pt-4 text-sm">
                <p><b>Probable Cause:</b> {analysis[inc.id].probable_cause}</p>
                <p className="mt-2"><b>Summary:</b> {analysis[inc.id].summary}</p>
                <p className="mt-2"><b>Recommendations:</b></p>
                <ul className="list-disc ml-5">
                  {analysis[inc.id].recommendation.map((r, i) => <li key={i}>{r}</li>)}
                </ul>
              </div>
            )}
          </div>
        ))}
        {incidents?.length === 0 && <p className="text-gray-500">No incidents yet.</p>}
      </div>
    </div>
  );
}