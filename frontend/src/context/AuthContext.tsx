import { createContext, useContext, useState, useEffect } from "react";
import API from "../services/api";

interface User {
  id: number;
  email: string;
  tenant_id: number;
  role: string;
  plan: string; // ✅ "free" | "pro"
}

interface AuthContextType {
  user: User | null;
  login: (email: string, password: string) => Promise<void>;
  logout: () => void;
  refreshUser: () => Promise<void>;
  loading: boolean;
}

const AuthContext = createContext<AuthContextType | null>(null);

export const AuthProvider = ({ children }: any) => {
  const [user, setUser] = useState<User | null>(null);
  const [loading, setLoading] = useState(true);

  // 🔥 Single source of truth
  const loadUser = async () => {
    try {
      const res = await API.get("/users/me");

      // ensure new object reference for re-render
      setUser({ ...res.data });
    } catch {
      setUser(null);
    }
  };

  const initializeAuth = async () => {
    if (localStorage.getItem("access_token")) {
      await loadUser();
    }
    setLoading(false);
  };

  // ✅ Used after upgrade
  const refreshUser = async () => {
    await loadUser();
  };

  const login = async (email: string, password: string) => {
    const formData = new URLSearchParams();
    formData.append("username", email);
    formData.append("password", password);

    const response = await API.post("/users/login", formData, {
      headers: { "Content-Type": "application/x-www-form-urlencoded" },
    });

    localStorage.setItem("access_token", response.data.access_token);
    await loadUser();
  };

  const logout = () => {
    localStorage.removeItem("access_token");
    setUser(null);
    window.location.href = "/login";
  };

  useEffect(() => {
    initializeAuth();
  }, []);

  return (
    <AuthContext.Provider
      value={{
        user,
        login,
        logout,
        refreshUser,
        loading,
      }}
    >
      {children}
    </AuthContext.Provider>
  );
};

export const useAuth = () => {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error("useAuth must be used inside AuthProvider");
  }
  return context;
};