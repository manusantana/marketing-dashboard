import { useEffect, useState } from "react";
import client from "../api/client";
import { BarChart, Bar, XAxis, YAxis, Tooltip, Legend, ResponsiveContainer } from "recharts";

export default function Dashboard() {
  const [kpis, setKpis] = useState(null);

  useEffect(() => {
    client.get("/kpis/basic")
      .then(res => setKpis(res.data))
      .catch(err => console.error(err));
  }, []);

  if (!kpis) return <p className="p-4">Cargando KPIs...</p>;

  const data = [
    { name: "Turnover", value: kpis.turnover },
    { name: "Margin", value: kpis.margin }
  ];

  return (
    <div className="p-6">
      <h2 className="text-xl font-bold mb-4">KPIs Básicos</h2>
      <ResponsiveContainer width="100%" height={300}>
        <BarChart data={data}>
          <XAxis dataKey="name" />
          <YAxis />
          <Tooltip />
          <Legend />
          <Bar dataKey="value" fill="#6366F1" />
        </BarChart>
      </ResponsiveContainer>
    </div>
  );
}