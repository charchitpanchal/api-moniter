import { useAuth } from "../context/AuthContext";
import MonitoredApis from "./MonitoredApis";

export default function Dashboard() {
  const { logout } = useAuth();
  return (
    <div>
      <div className="flex justify-between items-center p-8 pb-0">
        <h1 className="text-2xl font-bold">Dashboard</h1>
        <button onClick={logout} className="bg-red-500 text-white px-4 py-2 rounded">Logout</button>
      </div>
      <MonitoredApis />
    </div>
  );
}