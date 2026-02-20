export default function AdminUsersTable({ users }: any) {
  return (
    <table className="w-full bg-gray-900 rounded-xl">
      <thead>
        <tr className="text-left text-gray-400">
          <th className="p-4">Email</th>
          <th className="p-4">Plan</th>
          <th className="p-4">Role</th>
        </tr>
      </thead>
      <tbody>
        {users.map((u: any) => (
          <tr key={u.id} className="border-t border-gray-800">
            <td className="p-4">{u.email}</td>
            <td className="p-4">{u.plan}</td>
            <td className="p-4">{u.role}</td>
          </tr>
        ))}
      </tbody>
    </table>
  );
}