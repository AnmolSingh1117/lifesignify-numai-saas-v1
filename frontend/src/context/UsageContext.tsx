import { createContext, useContext, useEffect, useState } from "react";
import { getUsage } from "../services/usageService";
import { useAuth } from "./AuthContext";

interface Usage {
  reports_used: number;
  reports_limit: number;
}

const PLAN_LIMITS: Record<string, number> = {
  basic: 1,
  pro: 5,
  premium: 50,
};

const UsageContext = createContext<{
  usage: Usage | null;
  refreshUsage: () => void;
} | null>(null);

export const UsageProvider = ({ children }: any) => {
  const { user } = useAuth();
  const [usage, setUsage] = useState<Usage | null>(null);

  const loadUsage = async () => {
    if (!user) return;

    try {
      const data = await getUsage();
      setUsage(data);
    } catch {
      if (user.subscription) {
        setUsage({
          reports_used: user.subscription.reports_used,
          reports_limit:
            PLAN_LIMITS[user.subscription.plan_name?.toLowerCase()] ?? 0,
        });
      }
    }
  };

  useEffect(() => {
    if (user) {
      loadUsage();
    } else {
      setUsage(null);
    }
  }, [user]);

  return (
    <UsageContext.Provider value={{ usage, refreshUsage: loadUsage }}>
      {children}
    </UsageContext.Provider>
  );
};

export const useUsage = () => {
  const ctx = useContext(UsageContext);
  if (!ctx) throw new Error("useUsage must be inside UsageProvider");
  return ctx;
};