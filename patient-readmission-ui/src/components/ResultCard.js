import React from "react";

export default function ResultCard({ result }) {
  if (!result) {
    return (
      <div className="bg-white p-6 rounded-lg shadow text-center text-slate-500">
        No prediction yet — enter patient data and click Predict.
      </div>
    );
  }

  const percent = (result.prediction * 100).toFixed(2);
  const band = result.prediction >= 0.7 ? "High" : result.prediction >= 0.3 ? "Medium" : "Low";
  const color =
    band === "High" ? "bg-red-100 text-red-700" : band === "Medium" ? "bg-yellow-100 text-yellow-700" : "bg-green-100 text-green-700";

  return (
    <div className="bg-white p-6 rounded-lg shadow">
      <h4 className="text-lg font-semibold mb-2">Prediction Result</h4>

      <div className={`p-4 rounded ${color} inline-block`}>
        <div className="text-3xl font-bold">{percent}%</div>
        <div className="text-sm mt-1">Readmission risk ({band})</div>
      </div>

      <div className="mt-4 text-sm text-slate-600">
        <div>Raw score: {result.raw}</div>
      </div>
    </div>
  );
}
