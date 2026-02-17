import { useEffect } from "react";

declare global {
  interface Window {
    Razorpay: any;
  }
}

export default function UpgradePage() {

  useEffect(() => {
    const script = document.createElement("script");
    script.src = "https://checkout.razorpay.com/v1/checkout.js";
    script.async = true;
    document.body.appendChild(script);
  }, []);

  const handlePayment = () => {
    const options = {
      key: "rzp_test_xxxxx", // replace
      amount: 49900,
      currency: "INR",
      name: "Life Signify NumAI",
      description: "Pro Plan Upgrade",
      handler: function (response: any) {
        alert("Payment Successful!");
        console.log(response);
      },
      theme: {
        color: "#6366f1",
      },
    };

    const rzp = new window.Razorpay(options);
    rzp.open();
  };

  return (
    <div className="min-h-screen bg-black flex items-center justify-center text-white">
      <div className="bg-white/5 p-10 rounded-2xl border border-white/10 text-center space-y-6">

        <h1 className="text-3xl font-bold text-purple-400">
          Upgrade to Pro
        </h1>

        <p className="text-gray-400">
          Unlock unlimited AI reports, premium PDF exports,
          strategic intelligence layers and advanced analytics.
        </p>

        <button
          onClick={handlePayment}
          className="bg-gradient-to-r from-indigo-600 to-purple-600 px-8 py-3 rounded-xl"
        >
          Upgrade Now – ₹499
        </button>
      </div>
    </div>
  );
}
