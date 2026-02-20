import { Navigate } from "react-router-dom";
import { useAuth } from "../context/AuthContext";

interface PlanRouteProps {
  children: React.ReactNode;
}

export default function PlanRoute({ children }: PlanRouteProps) {
  const { user, loading } = useAuth();

  // Wait until auth state resolves
  if (loading) {
    return (
      <div className="flex items-center justify-center h-screen">
        Loading...
      </div>
    );
  }

  // Not logged in
  if (!user) {
    return <Navigate to="/login" replace />;
  }

  // Not Pro user
  if (user.plan !== "pro") {
    return <Navigate to="/upgrade" replace />;
  }

  return <>{children}</>;
}