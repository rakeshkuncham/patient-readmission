import React, { useState } from "react";
import Sidebar from "../components/Sidebar";
import Topbar from "../components/Topbar";
import PatientForm from "../components/PatientForm";
import ResultCard from "../components/ResultCard";
import RiskChart from "../components/RiskChart";

export default function Dashboard() {
  const [result, setResult] = useState(null);

  return (
    <div className="flex">
      <Sidebar />
      <div className="flex-1 min-h-screen">
        <Topbar>
          <div className="text-sm text-slate-500">AWS SageMaker · Live</div>
        </Topbar>

        <main className="p-6 grid grid-cols-1 lg:grid-cols-3 gap-6">
          <div className="lg:col-span-2 space-y-6">
            <PatientForm onResult={setResult} />
            {/* You can add more cards like patient history, logs, etc. */}
          </div>

          <div className="space-y-6">
            <ResultCard result={result} />
            <RiskChart score={result ? result.prediction : 0} />
          </div>
        </main>
      </div>
    </div>
  );
}
