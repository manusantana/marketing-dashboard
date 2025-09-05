export default function Navbar() {
  return (
    <nav className="navbar">
      <h1 className="font-bold">📊 Marketing Analytics</h1>
      <div className="flex gap-4">
        <a href="/" className="nav-link">Dashboard</a>
        <a href="/upload" className="nav-link">Upload</a>
      </div>
    </nav>
  );
}
