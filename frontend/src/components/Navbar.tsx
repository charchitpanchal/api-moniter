import { Link, useLocation } from "react-router-dom";
import { useAuth } from "../context/AuthContext";

export default function Navbar() {
  const { logout } = useAuth();
  const { pathname } = useLocation();

  const linkClass = (path: string) =>
    `px-3 py-2 rounded text-sm font-medium ${
      pathname === path ? "bg-blue-600 text-white" : "text-gray-600 hover:bg-gray-100"
    }`;

  return (
    <nav className="bg-white border-b sticky top-0 z-10">
      <div className="max-w-6xl mx-auto flex justify-between items-center px-6 py-3">
        <div className="flex items-center gap-2">
          <span className="font-bold text-lg text-blue-600">API Monitor</span>
          <Link to="/dashboard" className={linkClass("/dashboard")}>Dashboard</Link>
          <Link to="/incidents" className={linkClass("/incidents")}>Incidents</Link>
        </div>
        <button onClick={logout} className="bg-red-500 hover:bg-red-600 text-white text-sm px-4 py-2 rounded">
          Logout
        </button>
      </div>
    </nav>
  );
}
