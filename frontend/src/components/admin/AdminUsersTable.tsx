interface Props {
  users: any[];
  onDelete: (id: number) => void;
  onRoleChange: (id: number, role: string) => void;
}

export default function AdminUsersTable({
  users,
  onDelete,
  onRoleChange,
}: Props) {
  if (!users.length) {
    return (
      <div className="text-gray-400">
        No users found in this organization.
      </div>
    );
  }

  return (
    <table className="w-full bg-gray-900 rounded-xl text-white">
      <thead>
        <tr className="text-left text-gray-400">
          <th className="p-4">Email</th>
          <th className="p-4">Role</th>
          <th className="p-4">Actions</th>
        </tr>
      </thead>

      <tbody>
        {users.map((u) => (
          <tr key={u.id} className="border-t border-gray-800">
            <td className="p-4">{u.email}</td>

            <td className="p-4">
              <select
                value={u.role}
                onChange={(e) =>
                  onRoleChange(u.id, e.target.value)
                }
                className="bg-gray-800 p-2 rounded"
              >
                <option value="admin">Admin</option>
                <option value="manager">Manager</option>
                <option value="user">User</option>
              </select>
            </td>

            <td className="p-4">
              <button
                onClick={() => onDelete(u.id)}
                className="bg-red-600 hover:bg-red-700 px-3 py-1 rounded"
              >
                Delete
              </button>
            </td>
          </tr>
        ))}
      </tbody>
    </table>
  );
}