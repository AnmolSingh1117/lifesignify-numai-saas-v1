// src/services/billingService.ts

import api from "./api";

const billingService = {
  getPlans: async () => {
    const res = await api.get("/api/payments/plans");
    return res.data;
  },

  getPaymentHistory: async () => {
    const res = await api.get("/api/payments/history");
    return res.data;
  },

  createOrder: async (planName: string) => {
    const res = await api.post("/api/payments/create-order", {
      plan: planName,
    });
    return res.data;
  },

  verifyPayment: async (paymentData: any) => {
    const res = await api.post("/api/payments/verify", paymentData);
    return res.data;
  },
};

export default billingService;