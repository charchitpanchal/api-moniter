import Navbar from "../components/Navbar";
import MonitoredApis from "./MonitoredApis";

export default function Dashboard() {
  return (
    <div className="min-h-screen bg-slate-50">
      <Navbar />
      <MonitoredApis />
    </div>
  );
}