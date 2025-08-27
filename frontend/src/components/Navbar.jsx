export default function Navbar() {
  return (
    <nav className="bg-indigo-600 text-white p-4 flex justify-between">
      <h1 className="font-bold">📊 Marketing Analytics</h1>
      <div className="space-x-4">
        <a href="/" className="hover:underline">Dashboard</a>
        <a href="/upload" className="hover:underline">Upload</a>
      </div>
    </nav>
  );
}