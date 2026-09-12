import { useState } from "react";
import { useIncidents, useAnalyzeIncident } from "../hooks/useIncidents";
import type { AiAnalysis } from "../api/incidents";
import Navbar from "../components/Navbar";

const severityColor: Record<string, string> = {
  LOW: "bg-slate-100 text-slate-600",
  MEDIUM: "bg-amber-100 text-amber-700",
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
    analyzeMutation.mutate(id, { onSuccess: (data) => setAnalysis((prev) => ({ ...prev, [id]: data })) });
  };

  return (
    <div className="min-h-screen bg-slate-50">
      <Navbar />
      <div className="max-w-6xl mx-auto p-8">
        <h2 className="text-2xl font-bold text-slate-800 mb-6">Incidents</h2>
        {isLoading && <p className="text-slate-500">Loading...</p>}
        <div className="space-y-4">
          {incidents?.map((inc) => (
            <div key={inc.id} className="bg-white rounded-xl shadow-sm border border-slate-200 p-5">
              <div className="flex justify-between items-center">
                <div className="flex items-center gap-3">
                  <span className={`px-2.5 py-1 rounded-full text-xs font-semibold ${severityColor[inc.severity]}`}>{inc.severity}</span>
                  <span className="font-semibold text-slate-800">API #{inc.api_id}</span>
                  <span className="text-xs text-slate-400 border border-slate-200 px-2 py-0.5 rounded-full">{inc.status}</span>
                </div>
                <button onClick={() => handleAnalyze(inc.id)} disabled={analyzeMutation.isPending && openId === inc.id}
                  className="bg-violet-600 hover:bg-violet-700 text-white text-sm px-4 py-2 rounded-lg font-medium transition disabled:opacity-50">
                  {analyzeMutation.isPending && openId === inc.id ? "Analyzing..." : "✨ AI Analyze"}
                </button>
              </div>
              <p className="text-sm text-slate-500 mt-3">{inc.last_error}</p>

              {openId === inc.id && analysis[inc.id] && (
                <div className="mt-4 border-t border-slate-100 pt-4 text-sm space-y-3">
                  <p><span className="font-semibold text-slate-700">Probable Cause:</span> <span className="text-slate-600">{analysis[inc.id].probable_cause}</span></p>
                  <p><span className="font-semibold text-slate-700">Summary:</span> <span className="text-slate-600">{analysis[inc.id].summary}</span></p>
                  <div>
                    <p className="font-semibold text-slate-700 mb-1">Recommendations:</p>
                    <ul className="list-disc ml-5 text-slate-600 space-y-1">
                      {analysis[inc.id].recommendation.map((r, i) => <li key={i}>{r}</li>)}
                    </ul>
                  </div>
                </div>
              )}
            </div>
          ))}
          {incidents?.length === 0 && <p className="text-slate-400 text-center py-8">No incidents yet. Your APIs are healthy! 🎉</p>}
        </div>
      </div>
    </div>
  );
}