import { useEffect, useState } from "react";
import { useAuth } from "../../context/AuthContext";
import billingService from "../../services/billingService";
import toast from "react-hot-toast";

interface Plan {
  name: string;
  price: number;
  features: string[];
}

interface PaymentHistory {
  id: number;
  amount: number;
  status: string;
  created_at: string;
}

declare global {
  interface Window {
    Razorpay: any;
  }
}

export default function BillingPage() {
  const { user, refreshUser } = useAuth();
  const [plans, setPlans] = useState<Plan[]>([]);
  const [payments, setPayments] = useState<PaymentHistory[]>([]);
  const [loading, setLoading] = useState(true);
  const [upgrading, setUpgrading] = useState(false);

  useEffect(() => {
    const loadBillingData = async () => {
      try {
        const plansRes = await billingService.getPlans();
        const paymentRes = await billingService.getPaymentHistory();

        setPlans(plansRes);
        setPayments(paymentRes);
      } catch {
        toast.error("Failed to load billing data");
      } finally {
        setLoading(false);
      }
    };

    loadBillingData();
  }, []);

  const handleUpgrade = async (planName: string) => {
    if (upgrading) return;

    setUpgrading(true);

    try {
      // 1️⃣ Create Razorpay order from backend
      const order = await billingService.createOrder(planName);

      const options = {
        key: import.meta.env.VITE_RAZORPAY_KEY,
        amount: order.amount,
        currency: "INR",
        order_id: order.id,
        name: "LifeSignify",
        description: `${planName} Subscription`,
        handler: async function (response: any) {
          try {
            // 2️⃣ Verify payment
            await billingService.verifyPayment(response);

            // 3️⃣ Refresh user plan
            await refreshUser();

            toast.success("Subscription upgraded successfully 🚀");
          } catch {
            toast.error("Payment verification failed");
          }
        },
        theme: {
          color: "#6366f1",
        },
      };

      const razor = new window.Razorpay(options);
      razor.open();

    } catch (error: any) {
      toast.error(error?.response?.data?.detail || "Payment failed");
    } finally {
      setUpgrading(false);
    }
  };

  if (loading) {
    return (
      <div className="min-h-screen bg-gray-950 text-white flex items-center justify-center">
        Loading Billing...
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-950 text-white p-8 space-y-10">

      {/* Header */}
      <div>
        <h1 className="text-3xl font-bold">Subscription & Billing</h1>
        <p className="text-gray-400 mt-1">
          Manage your subscription and payments
        </p>
      </div>

      {/* Current Plan */}
      <div className="bg-gray-900 p-6 rounded-xl shadow-md">
        <p className="text-gray-400 text-sm">Current Plan</p>
        <p className="text-2xl font-bold mt-2">
          {user?.plan?.toUpperCase() || "FREE"}
        </p>
      </div>

      {/* Plans */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        {plans.map((plan) => (
          <div
            key={plan.name}
            className="bg-gray-900 p-6 rounded-xl shadow-md flex flex-col justify-between"
          >
            <div>
              <h2 className="text-xl font-semibold">{plan.name}</h2>
              <p className="text-3xl font-bold mt-2">
                ₹{plan.price}
                <span className="text-sm text-gray-400"> / month</span>
              </p>

              <ul className="mt-4 space-y-2 text-gray-300 text-sm">
                {plan.features.map((feature, index) => (
                  <li key={index}>• {feature}</li>
                ))}
              </ul>
            </div>

            {user?.plan !== plan.name.toLowerCase() && (
              <button
                onClick={() => handleUpgrade(plan.name)}
                disabled={upgrading}
                className="mt-6 bg-indigo-600 hover:bg-indigo-500 p-3 rounded-lg font-semibold transition disabled:opacity-50"
              >
                Upgrade
              </button>
            )}
          </div>
        ))}
      </div>

      {/* Payment History */}
      <div className="bg-gray-900 p-6 rounded-xl shadow-md">
        <h2 className="text-xl font-semibold mb-4">
          Payment History
        </h2>

        {payments.length === 0 ? (
          <p className="text-gray-400">No payments found.</p>
        ) : (
          <table className="w-full text-left text-sm">
            <thead>
              <tr className="text-gray-400 border-b border-gray-800">
                <th className="py-2">Date</th>
                <th className="py-2">Amount</th>
                <th className="py-2">Status</th>
              </tr>
            </thead>
            <tbody>
              {payments.map((payment) => (
                <tr key={payment.id} className="border-b border-gray-800">
                  <td className="py-2">
                    {new Date(payment.created_at).toLocaleDateString()}
                  </td>
                  <td className="py-2">₹{payment.amount}</td>
                  <td
                    className={`py-2 ${
                      payment.status === "success"
                        ? "text-emerald-400"
                        : "text-yellow-400"
                    }`}
                  >
                    {payment.status}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        )}
      </div>
    </div>
  );
}