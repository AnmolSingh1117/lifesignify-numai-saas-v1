import { useEffect, useState } from "react";
import { fetchAllUsers } from "../../services/adminService";
import AdminUsersTable from "../../components/admin/AdminUsersTable";

export default function AdminUsersPage() {
  const [users, setUsers] = useState<any[]>([]);

  useEffect(() => {
    fetchAllUsers().then(setUsers);
  }, []);

  return (
    <div className="p-8">
      <AdminUsersTable users={users} />
    </div>
  );
}