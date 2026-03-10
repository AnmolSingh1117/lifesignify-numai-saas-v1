import { useState } from "react";
import { useNavigate } from "react-router-dom";
import API from "../../services/api";
import { useAuth } from "../../context/AuthContext";
import toast from "react-hot-toast";

declare global {
  interface Window {
    Razorpay: any;
  }
}

export default function UpgradePage() {
  const { user, refreshUser } = useAuth();
  const navigate = useNavigate();
  const [loading, setLoading] = useState(false);

  const handleUpgrade = async () => {
    // ✅ FIXED: use organization.plan
    if (loading || user?.organization?.plan === "pro") return;

    setLoading(true);

    try {
      const orderRes = await API.post("/payments/create-order", {
        plan: "pro",
      });

      const { id, amount, currency } = orderRes.data;

      const options = {
        key: import.meta.env.VITE_RAZORPAY_KEY,
        amount,
        currency,
        name: "Life Signify NumAI",
        description: "Pro Subscription",
        order_id: id,

        handler: async function (response: any) {
          const verifyToast = toast.loading("Verifying payment...");

          try {
            await API.post("/payments/verify", {
              razorpay_order_id: response.razorpay_order_id,
              razorpay_payment_id: response.razorpay_payment_id,
              razorpay_signature: response.razorpay_signature,
            });

            await refreshUser();

            toast.success("Subscription activated 🎉", {
              id: verifyToast,
            });

            navigate("/dashboard");
          } catch (error: any) {
            toast.error(
              error?.response?.data?.detail?.[0]?.msg ||
                error?.response?.data?.detail ||
                "Payment verification failed",
              { id: verifyToast }
            );
          } finally {
            setLoading(false);
          }
        },

        modal: {
          ondismiss: function () {
            setLoading(false);
          },
        },

        theme: {
          color: "#6366F1",
        },
      };

      const rzp = new window.Razorpay(options);
      rzp.open();
    } catch (error: any) {
      toast.error(
        error?.response?.data?.detail?.[0]?.msg ||
          error?.response?.data?.detail ||
          "Failed to create order"
      );
      setLoading(false);
    }
  };

  const isPro = user?.organization?.plan === "pro";

  return (
    <div className="min-h-screen bg-gray-950 text-white p-8 flex items-center justify-center">
      <div className="bg-gray-900 p-10 rounded-xl w-full max-w-md space-y-6 text-center">

        <h1 className="text-3xl font-bold">Upgrade to Pro</h1>

        <p className="text-gray-400">
          Unlock full AI strategic analysis and premium insights.
        </p>

        <div className="bg-gray-800 p-6 rounded-xl">
          <p className="text-xl font-semibold">₹999 / month</p>
          <p className="text-sm text-gray-400 mt-2">
            Cancel anytime
          </p>
        </div>

        <button
          onClick={handleUpgrade}
          disabled={loading || isPro}
          className="bg-emerald-600 hover:bg-emerald-500 w-full py-3 rounded-lg font-semibold transition disabled:opacity-50 disabled:cursor-not-allowed"
        >
          {isPro
            ? "Already on Pro Plan"
            : loading
            ? "Processing..."
            : "Upgrade Now"}
        </button>

        {isPro && (
          <div className="text-emerald-400 font-semibold">
            🎉 You are already on Pro Plan
          </div>
        )}
      </div>
    </div>
  );
}