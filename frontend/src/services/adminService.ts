import API from "./api";

export const fetchAdminAnalytics = async () => {
  const res = await API.get("/admin/analytics");
  return res.data;
};

export const fetchAllUsers = async () => {
  const res = await API.get("/admin/users");
  return res.data;
};