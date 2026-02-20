const Sidebar = () => {
  return (
    <div className="w-64 bg-gray-900 text-white min-h-screen p-4">
      <h2 className="text-xl font-bold mb-6">LifeSignify</h2>

      <nav className="space-y-3">
        <a href="/dashboard" className="block hover:text-indigo-400">
          Dashboard
        </a>
        <a href="/reports" className="block hover:text-indigo-400">
          Reports
        </a>
        <a href="/billing" className="block hover:text-indigo-400">
          Billing
        </a>
        <a href="/settings" className="block hover:text-indigo-400">
          Settings
        </a>
      </nav>
    </div>
  );
};

export default Sidebar;