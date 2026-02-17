import { Routes, Route } from "react-router-dom";
import DashboardPage from "../pages/dashboard/DashboardPage";
import UpgradePage from "../pages/upgrade/UpgradePage";
import LoginPage from "../pages/auth/LoginPage";
import ProtectedRoute from "../components/ProtectedRoute";

export default function AppRoutes() {
  return (
    <Routes>
      {/* Public */}
      <Route path="/login" element={<LoginPage />} />

      {/* Protected */}
      <Route
        path="/"
        element={
          <ProtectedRoute>
            <DashboardPage />
          </ProtectedRoute>
        }
      />

      <Route
        path="/upgrade"
        element={
          <ProtectedRoute>
            <UpgradePage />
          </ProtectedRoute>
        }
      />
    </Routes>
  );
}
