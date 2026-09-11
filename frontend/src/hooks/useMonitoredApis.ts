import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";
import {
  listMonitoredApis,
  createMonitoredApi,
  deleteMonitoredApi,
  toggleMonitoredApi,
  type MonitoredApiCreate,
} from "../api/monitoredApis";

export function useMonitoredApis() {
  return useQuery({
    queryKey: ["monitoredApis"],
    queryFn: listMonitoredApis,
    refetchInterval: 10000,
  });
}

export function useCreateMonitoredApi() {
  const qc = useQueryClient();
  return useMutation({
    mutationFn: (payload: MonitoredApiCreate) => createMonitoredApi(payload),
    onSuccess: () => qc.invalidateQueries({ queryKey: ["monitoredApis"] }),
  });
}

export function useDeleteMonitoredApi() {
  const qc = useQueryClient();
  return useMutation({
    mutationFn: (id: number) => deleteMonitoredApi(id),
    onSuccess: () => qc.invalidateQueries({ queryKey: ["monitoredApis"] }),
  });
}

export function useToggleMonitoredApi() {
  const qc = useQueryClient();
  return useMutation({
    mutationFn: ({ id, enable }: { id: number; enable: boolean }) => toggleMonitoredApi(id, enable),
    onSuccess: () => qc.invalidateQueries({ queryKey: ["monitoredApis"] }),
  });
}