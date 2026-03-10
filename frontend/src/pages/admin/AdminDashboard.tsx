import { useEffect, useState } from "react";
import {
  fetchOrgUsers,
  deleteUser,
  updateUserRole,
  inviteUser,
} from "../../services/adminService";
import AdminUsersTable from "../../components/admin/AdminUsersTable";

export default function AdminUsersPage() {
  const [users, setUsers] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);

  // Invite state
  const [inviteEmail, setInviteEmail] = useState("");
  const [inviteRole, setInviteRole] = useState("user");
  const [inviteLoading, setInviteLoading] = useState(false);

  const loadUsers = async () => {
    try {
      const data = await fetchOrgUsers();
      setUsers(data);
    } catch (error) {
      console.error("Failed to fetch users");
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadUsers();
  }, []);

  const handleDelete = async (id: number) => {
    await deleteUser(id);
    loadUsers();
  };

  const handleRoleChange = async (id: number, role: string) => {
    await updateUserRole(id, role);
    loadUsers();
  };

  const handleInvite = async () => {
    if (!inviteEmail) return;

    setInviteLoading(true);
    try {
      const res = await inviteUser(inviteEmail, inviteRole);
      alert(
        `User invited successfully.\nTemporary password: ${res.temporary_password}`
      );
      setInviteEmail("");
      setInviteRole("user");
      loadUsers();
    } catch (err: any) {
      alert(err?.response?.data?.detail || "Failed to invite user");
    } finally {
      setInviteLoading(false);
    }
  };

  if (loading) {
    return <div className="p-8 text-white">Loading users...</div>;
  }

  return (
    <div className="p-8">
      <h1 className="text-2xl text-white mb-6">Organization Users</h1>

      {/* Invite Section */}
      <div className="bg-gray-900 p-4 rounded-xl mb-6 flex gap-4 items-center">
        <input
          type="email"
          placeholder="Enter email"
          value={inviteEmail}
          onChange={(e) => setInviteEmail(e.target.value)}
          className="bg-gray-800 px-4 py-2 rounded text-white w-64"
        />

        <select
          value={inviteRole}
          onChange={(e) => setInviteRole(e.target.value)}
          className="bg-gray-800 px-4 py-2 rounded text-white"
        >
          <option value="user">User</option>
          <option value="manager">Manager</option>
          <option value="admin">Admin</option>
        </select>

        <button
          onClick={handleInvite}
          disabled={inviteLoading}
          className="bg-indigo-600 px-6 py-2 rounded hover:bg-indigo-700"
        >
          Invite User
        </button>
      </div>

      <AdminUsersTable
        users={users}
        onDelete={handleDelete}
        onRoleChange={handleRoleChange}
      />
    </div>
  );
}