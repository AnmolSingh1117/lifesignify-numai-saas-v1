import { Link, useLocation } from "react-router-dom";
import { useAuth } from "../../context/AuthContext";

const Sidebar = () => {
  const { user } = useAuth();
  const location = useLocation();

  const linkClass = (path: string) =>
    `block px-3 py-2 rounded transition ${
      location.pathname.startsWith(path)
        ? "bg-gray-800 text-white"
        : "text-gray-400 hover:text-indigo-400"
    }`;

  return (
    <div className="w-64 bg-gray-900 text-white min-h-screen p-4">
      <h2 className="text-xl font-bold mb-6">LifeSignify</h2>

      <nav className="space-y-2">
        <Link to="/dashboard" className={linkClass("/dashboard")}>
          Dashboard
        </Link>

        <Link to="/reports" className={linkClass("/reports")}>
          Reports
        </Link>

        <Link to="/billing" className={linkClass("/billing")}>
          Billing
        </Link>

        <Link to="/settings" className={linkClass("/settings")}>
          Settings
        </Link>

        {/* 🔥 ADMIN LINK (only visible to admins) */}
        {user?.role === "admin" && (
          <Link to="/admin/users" className={linkClass("/admin")}>
            Admin
          </Link>
        )}
      </nav>
    </div>
  );
};

export default Sidebar;