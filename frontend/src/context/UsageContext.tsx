import { createContext, useContext, useEffect, useState } from "react";
import { getUsage } from "../services/usageService";

interface Usage {
  reports_used: number;
  reports_limit: number;
}

const UsageContext = createContext<{
  usage: Usage | null;
  refreshUsage: () => void;
} | null>(null);

export const UsageProvider = ({ children }: any) => {
  const [usage, setUsage] = useState<Usage | null>(null);

  const loadUsage = async () => {
    const data = await getUsage();
    setUsage(data);
  };

  useEffect(() => {
    loadUsage();
  }, []);

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