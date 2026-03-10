import { useAuth } from "../../context/AuthContext";

export default function SettingsPage() {
  const { user } = useAuth();

  // 🔥 Proper plan resolution (subscription first, then org fallback)
  const plan =
    user?.subscription?.plan_name ||
    user?.organization?.plan ||
    "FREE";

  const isActive = user?.subscription?.is_active;

  return (
    <div className="min-h-screen bg-gray-950 text-white p-8 space-y-8">
      
      {/* Header */}
      <div>
        <h1 className="text-3xl font-bold">Settings</h1>
        <p className="text-gray-400 mt-1">
          Manage your account preferences
        </p>
      </div>

      {/* Profile Card */}
      <div className="bg-gray-900 p-6 rounded-xl shadow-md">
        <h2 className="text-xl font-semibold mb-4">Account Info</h2>

        <div className="space-y-3 text-gray-300">
          <p>
            <span className="text-gray-400">Email:</span> {user?.email}
          </p>

          <p>
            <span className="text-gray-400">Plan:</span>{" "}
            <span
              className={`font-semibold ml-1 ${
                plan.toLowerCase() === "pro"
                  ? "text-emerald-400"
                  : plan.toLowerCase() === "enterprise"
                  ? "text-purple-400"
                  : "text-gray-300"
              }`}
            >
              {plan.toUpperCase()}
            </span>
          </p>

          {isActive && (
            <p className="text-sm text-green-400">
              Active Subscription
            </p>
          )}
        </div>
      </div>

      {/* Future Settings Placeholder */}
      <div className="bg-gray-900 p-6 rounded-xl shadow-md">
        <h2 className="text-xl font-semibold mb-2">
          Preferences
        </h2>
        <p className="text-gray-400 text-sm">
          Notification settings, password updates, and integrations
          will be available here.
        </p>
      </div>
    </div>
  );
}