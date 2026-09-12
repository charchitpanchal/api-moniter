import { useQuery } from "@tanstack/react-query";
import { getMetrics, getChecks } from "../api/metrics";

export function useMetrics(id: number) {
  return useQuery({ queryKey: ["metrics", id], queryFn: () => getMetrics(id), refetchInterval: 15000 });
}

export function useChecks(id: number) {
  return useQuery({ queryKey: ["checks", id], queryFn: () => getChecks(id), refetchInterval: 15000 });
}