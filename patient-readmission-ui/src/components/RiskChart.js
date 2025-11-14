import React from "react";
import { PieChart, Pie, Cell, ResponsiveContainer, Legend } from "recharts";

const COLORS = ["#10B981", "#F59E0B", "#EF4444"];

export default function RiskChart({ score = 0.0 }) {
  const data = [
    { name: "Low", value: Math.max(0, 1 - score) },
    { name: "High", value: score }
  ];

  return (
    <div className="bg-white p-6 rounded-lg shadow">
      <h4 className="text-lg font-semibold mb-4">Risk Distribution</h4>
      <div style={{ width: "100%", height: 200 }}>
        <ResponsiveContainer>
          <PieChart>
            <Pie data={data} dataKey="value" innerRadius={50} outerRadius={80} paddingAngle={4}>
              {data.map((entry, index) => (
                <Cell key={entry.name} fill={index === 0 ? COLORS[0] : COLORS[2]} />
              ))}
            </Pie>
            <Legend />
          </PieChart>
        </ResponsiveContainer>
      </div>
    </div>
  );
}
