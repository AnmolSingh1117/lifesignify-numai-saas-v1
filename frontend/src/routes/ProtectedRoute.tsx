import { Navigate } from "react-router-dom";
import { useAuth } from "../context/AuthContext";

interface ProtectedRouteProps {
  children: React.ReactNode;
  requirePro?: boolean;
}

const ProtectedRoute = ({ children, requirePro = false }: ProtectedRouteProps) => {
  const { user, loading } = useAuth();

  // Wait until auth is resolved
  if (loading) {
    return <div style={{ textAlign: "center", marginTop: "50px" }}>Loading...</div>;
  }

  // Not logged in
  if (!user) {
    return <Navigate to="/login" replace />;
  }

  // Pro feature protection
  if (requirePro && user.plan_type !== "pro") {
    return <Navigate to="/upgrade" replace />;
  }

  return <>{children}</>;
};

export default ProtectedRoute;