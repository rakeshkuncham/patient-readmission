import React from "react";

export default function Topbar({ children }) {
  return (
    <header className="bg-white border-b px-6 py-4 flex items-center justify-between">
      <div className="flex items-center gap-4">
        <button className="md:hidden p-2 rounded-lg bg-slate-100">☰</button>
        <h3 className="text-lg font-semibold text-slate-800">Patient Readmission Dashboard</h3>
      </div>

      <div className="flex items-center gap-4">
        {children}
        <div className="flex items-center gap-2 p-2 rounded-md bg-slate-100">
          <img src={`https://ui-avatars.com/api/?name=RK&background=0D9488&color=fff`} alt="avatar" className="w-8 h-8 rounded-full"/>
          <div className="text-sm">
            <div className="font-medium">Rakesh</div>
            <div className="text-xs text-slate-500">DevOps · AWS</div>
          </div>
        </div>
      </div>
    </header>
  );
}
