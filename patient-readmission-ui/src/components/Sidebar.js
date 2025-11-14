import React from "react";
import { NavLink } from "react-router-dom";

export default function Sidebar() {
  const navClass = ({ isActive }) =>
    `flex items-center gap-3 px-4 py-3 rounded-md ${
      isActive ? "bg-blue-600 text-white" : "text-slate-700 hover:bg-slate-100"
    }`;

  return (
    <aside className="w-72 bg-white h-screen border-r p-6 hidden md:block">
      <div className="mb-8">
        <h2 className="text-2xl font-bold text-blue-600">Service · Readmit</h2>
        <p className="text-sm text-slate-500 mt-1">Patient risk prediction</p>
      </div>

      <nav className="space-y-2">
        <NavLink to="/" className={navClass} end>
          Dashboard
        </NavLink>
        <NavLink to="/about" className={navClass}>
          About
        </NavLink>
      </nav>

      <div className="mt-8 text-xs text-slate-500">
        <p>Logged in as</p>
        <p className="font-medium text-slate-800 mt-1">Rakesh Kuncham</p>
      </div>
    </aside>
  );
}
