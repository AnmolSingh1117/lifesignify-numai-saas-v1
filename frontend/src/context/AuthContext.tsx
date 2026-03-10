import {
  createContext,
  useContext,
  useState,
  useEffect,
  useRef,
  useCallback,
} from "react";
import API from "../services/api";

interface User {
  id: number;
  email: string;
  role: string;
  organization: {
    id: number;
    name: string;
    plan: string;
  };
  subscription: {
    plan_name: string;
    is_active: boolean;
    end_date: string | null;
    reports_used: number;
  };
}

interface AuthContextType {
  user: User | null;
  login: (email: string, password: string) => Promise<void>;
  logout: () => void;
  refreshUser: () => Promise<void>;
  loading: boolean;
}

const AuthContext = createContext<AuthContextType | null>(null);

export const AuthProvider = ({ children }: { children: React.ReactNode }) => {
  const [user, setUser] = useState<User | null>(null);
  const [loading, setLoading] = useState(true);

  const initialized = useRef(false);
  const loadingUser = useRef(false); // prevents parallel calls

  const loadUser = useCallback(async () => {
    if (loadingUser.current) return; // prevent duplicate calls
    loadingUser.current = true;

    try {
      const res = await API.get("/users/me");
      setUser(res.data);
    } catch {
      localStorage.removeItem("access_token");
      setUser(null);
    } finally {
      loadingUser.current = false;
    }
  }, []);

  const initializeAuth = useCallback(async () => {
    if (initialized.current) return; // StrictMode safe
    initialized.current = true;

    const token = localStorage.getItem("access_token");

    if (!token) {
      setLoading(false);
      return;
    }

    await loadUser();
    setLoading(false);
  }, [loadUser]);

  const refreshUser = async () => {
    await loadUser();
  };

  const login = async (email: string, password: string) => {
    const formData = new URLSearchParams();
    formData.append("username", email);
    formData.append("password", password);

    const response = await API.post("/users/login", formData, {
      headers: {
        "Content-Type": "application/x-www-form-urlencoded",
      },
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
  }, [initializeAuth]);

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