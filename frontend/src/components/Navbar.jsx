import { NavLink } from "react-router-dom";

export default function Navbar() {
  const baseLink =
    "px-3 py-2 rounded-md transition-colors hover:bg-indigo-500";
  const activeLink = "bg-indigo-700";

  return (
    <nav className="bg-indigo-600 text-white p-4 flex justify-between items-center shadow">
      <h1 className="font-bold text-lg">📊 Marketing Analytics</h1>
      <div className="space-x-2">
        <NavLink
          to="/"
          end
          className={({ isActive }) =>
            `${baseLink} ${isActive ? activeLink : ""}`
          }
        >
          Dashboard
        </NavLink>
        <NavLink
          to="/upload"
          className={({ isActive }) =>
            `${baseLink} ${isActive ? activeLink : ""}`
          }
        >
          Upload
        </NavLink>
      </div>
    </nav>
  );
}

