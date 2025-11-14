import React from "react";
import Sidebar from "../components/Sidebar";
import Topbar from "../components/Topbar";

export default function About() {
  return (
    <div className="flex">
      <Sidebar />
      <div className="flex-1 min-h-screen">
        <Topbar />
        <main className="p-8">
          <div className="max-w-3xl bg-white p-6 rounded-lg shadow">
            <h2 className="text-2xl font-bold mb-2">About Project</h2>
            <p className="text-slate-600 mb-4">
              AI-Powered Patient Readmission Risk Prediction. Built with AWS SageMaker for model training and real-time inference, API Gateway + Lambda for secure serving, and this React dashboard for clinicians.
            </p>

            <ul className="list-disc pl-6 text-slate-700">
              <li>Real-time predictions via SageMaker endpoint</li>
              <li>CI/CD and secure deployment (Jenkins / ECR)</li>
              <li>Monitoring via CloudWatch and Grafana</li>
            </ul>
          </div>
        </main>
      </div>
    </div>
  );
}
