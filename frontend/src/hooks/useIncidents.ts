import { useQuery, useMutation } from "@tanstack/react-query";
import { listIncidents, analyzeIncident } from "../api/incidents";

export function useIncidents() {
  return useQuery({
    queryKey: ["incidents"],
    queryFn: listIncidents,
    refetchInterval: 15000,
  });
}

export function useAnalyzeIncident() {
  return useMutation({ mutationFn: (id: number) => analyzeIncident(id) });
}