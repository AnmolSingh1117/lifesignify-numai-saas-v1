import { useState } from "react";
import { useNavigate, Link } from "react-router-dom";
import { useAuth } from "../../context/AuthContext";
import API from "../../services/api";
import toast from "react-hot-toast";

const RegisterPage = () => {
  const navigate = useNavigate();
  const { login } = useAuth();

  const [form, setForm] = useState({
    organization_name: "",
    email: "",
    password: "",
  });

  const [loading, setLoading] = useState(false);
  const [showPassword, setShowPassword] = useState(false);

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setForm({ ...form, [e.target.name]: e.target.value });
  };

  const validatePassword = (password: string) => {
    if (password.length < 6) {
      return "Password must be at least 6 characters";
    }
    return null;
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();

    if (loading) return;

    if (!form.organization_name || !form.email || !form.password) {
      toast.error("All fields are required");
      return;
    }

    const passwordError = validatePassword(form.password);
    if (passwordError) {
      toast.error(passwordError);
      return;
    }

    setLoading(true);
    const loadingToast = toast.loading("Creating account...");

    try {
      // 1️⃣ Register
      await API.post("/users/register", form);

      // 2️⃣ Auto login
      await login(form.email, form.password);

      toast.success("Welcome to Life Signify NumAI 🚀", {
        id: loadingToast,
      });

      // 3️⃣ Redirect to dashboard
      navigate("/dashboard");

    } catch (error: any) {
      toast.error(
        error?.response?.data?.detail || "Registration failed",
        { id: loadingToast }
      );
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen flex items-center justify-center bg-gray-950 text-white p-6">
      <form
        onSubmit={handleSubmit}
        className="bg-gray-900 p-8 rounded-2xl w-full max-w-md shadow-xl space-y-6"
      >
        <div className="text-center">
          <h1 className="text-3xl font-bold">
            Create Organization Account
          </h1>
          <p className="text-gray-400 mt-2">
            Start your Life Intelligence journey
          </p>
        </div>

        {/* Organization */}
        <div>
          <label className="text-sm text-gray-400">
            Organization Name
          </label>
          <input
            name="organization_name"
            value={form.organization_name}
            onChange={handleChange}
            className="w-full mt-1 p-3 bg-gray-800 rounded-lg border border-gray-700 focus:outline-none focus:ring-2 focus:ring-indigo-500"
            placeholder="Your Company Name"
          />
        </div>

        {/* Email */}
        <div>
          <label className="text-sm text-gray-400">Email</label>
          <input
            name="email"
            type="email"
            value={form.email}
            onChange={handleChange}
            className="w-full mt-1 p-3 bg-gray-800 rounded-lg border border-gray-700 focus:outline-none focus:ring-2 focus:ring-indigo-500"
            placeholder="you@example.com"
          />
        </div>

        {/* Password */}
        <div>
          <label className="text-sm text-gray-400">Password</label>
          <div className="relative">
            <input
              name="password"
              type={showPassword ? "text" : "password"}
              value={form.password}
              onChange={handleChange}
              className="w-full mt-1 p-3 bg-gray-800 rounded-lg border border-gray-700 focus:outline-none focus:ring-2 focus:ring-indigo-500 pr-12"
              placeholder="••••••••"
            />

            <button
              type="button"
              onClick={() => setShowPassword(!showPassword)}
              className="absolute right-3 top-1/2 -translate-y-1/2 text-sm text-gray-400 hover:text-white"
            >
              {showPassword ? "Hide" : "Show"}
            </button>
          </div>
        </div>

        {/* Submit */}
        <button
          type="submit"
          disabled={loading}
          className="w-full p-3 bg-indigo-600 hover:bg-indigo-500 rounded-lg font-semibold transition disabled:opacity-50"
        >
          {loading ? "Creating..." : "Register"}
        </button>

        {/* Login Link */}
        <div className="text-center text-sm text-gray-400">
          Already have an account?{" "}
          <Link
            to="/login"
            className="text-indigo-400 hover:underline"
          >
            Login
          </Link>
        </div>
      </form>
    </div>
  );
};

export default RegisterPage;