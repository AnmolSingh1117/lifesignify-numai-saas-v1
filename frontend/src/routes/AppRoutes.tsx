import { Routes, Route, Navigate } from "react-router-dom";
import { useAuth } from "../context/AuthContext";

import AppLayout from "../components/layout/AppLayout";

import DashboardPage from "../pages/dashboard/DashboardPage";
import ReportsListPage from "../pages/reports/ReportsListPage";
import ReportDetailPage from "../pages/reports/ReportDetailPage";
import GenerateReportPage from "../pages/reports/GenerateReportPage"; // ✅ NEW

import UpgradePage from "../pages/upgrade/UpgradePage";
import BillingPage from "../pages/billing/BillingPage";
import SettingsPage from "../pages/settings/SettingsPage";

import AdminDashboard from "../pages/admin/AdminDashboard";
import AdminUsersPage from "../pages/admin/AdminUsersPage";

import LoginPage from "../pages/auth/LoginPage";
import RegisterPage from "../pages/auth/RegisterPage";

import NotFoundPage from "../pages/errors/NotFoundPage";
import ForbiddenPage from "../pages/errors/ForbiddenPage";

import ProtectedRoute from "../components/ProtectedRoute";
import AdminRoute from "./AdminRoute";
import PlanRoute from "./PlanRoute";

export default function AppRoutes() {
  const { user, loading } = useAuth();

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-gray-950 text-white">
        Loading...
      </div>
    );
  }

  return (
    <Routes>
      {/* PUBLIC ROUTES */}
      <Route
        path="/login"
        element={user ? <Navigate to="/dashboard" replace /> : <LoginPage />}
      />

      <Route
        path="/register"
        element={user ? <Navigate to="/dashboard" replace /> : <RegisterPage />}
      />

      {/* PROTECTED ROUTES WITH LAYOUT */}
      <Route
        path="/"
        element={
          <ProtectedRoute>
            <AppLayout />
          </ProtectedRoute>
        }
      >
        <Route path="dashboard" element={<DashboardPage />} />
        <Route path="reports" element={<ReportsListPage />} />
        <Route path="reports/:id" element={<ReportDetailPage />} />
        
        {/* ✅ NEW ROUTE ADDED HERE */}
        <Route path="generate-report" element={<GenerateReportPage />} />

        <Route path="settings" element={<SettingsPage />} />
        <Route path="upgrade" element={<UpgradePage />} />

        {/* BILLING (Plan Protected) */}
        <Route
          path="billing"
          element={
            <PlanRoute>
              <BillingPage />
            </PlanRoute>
          }
        />

        {/* ADMIN ROUTES */}
        <Route
          path="admin"
          element={
            <AdminRoute>
              <AdminDashboard />
            </AdminRoute>
          }
        />

        <Route
          path="admin/users"
          element={
            <AdminRoute>
              <AdminUsersPage />
            </AdminRoute>
          }
        />
      </Route>

      {/* ERROR ROUTES */}
      <Route path="/forbidden" element={<ForbiddenPage />} />
      <Route path="*" element={<NotFoundPage />} />
    </Routes>
  );
}