import { useEffect, useState } from "react";
import { fetchAdminAnalytics } from "../../services/adminService";
import AdminStatsCard from "../../components/admin/AdminStatsCard";

export default function AdminDashboard() {
  const [data, setData] = useState<any>(null);

  useEffect(() => {
    fetchAdminAnalytics().then(setData);
  }, []);

  if (!data) return <div className="p-8">Loading...</div>;

  return (
    <div className="p-8 grid grid-cols-3 gap-6">
      <AdminStatsCard label="Total Users" value={data.total_users} />
      <AdminStatsCard label="Pro Users" value={data.pro_users} />
      <AdminStatsCard label="Revenue" value={`₹${data.total_revenue}`} />
    </div>
  );
}