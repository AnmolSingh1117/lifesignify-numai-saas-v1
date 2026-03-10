import API from "./api";

export const getUsage = async () => {
  const res = await API.get("/users/me");
  return {
    reports_used: res.data.reports_used || 0,
    reports_limit: res.data.reports_limit || 10,
  };
};