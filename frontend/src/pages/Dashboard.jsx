import { useEffect, useState } from "react";
import client from "../api/client";
import { BarChart, Bar, XAxis, YAxis, Tooltip, Legend, ResponsiveContainer } from "recharts";

export default function Dashboard() {
  const [kpis, setKpis] = useState(null);

  useEffect(() => {
    console.log("🚀 Pidiendo KPIs...");
    client.get("/kpis/basic")
      .then(res => {
        console.log("📊 KPIs recibidos:", res.data);
        setKpis(res.data);
      })
      .catch(err => console.error("❌ Error cargando KPIs:", err));
  }, []);

  if (!kpis) return <p className="p-4">Cargando KPIs...</p>;

  const data = [
    { name: "Turnover", value: kpis.ventas_totales },
    { name: "Ticket Medio", value: kpis.ticket_medio }
  ];

  return (
    <div className="p-6">
      <h2 className="text-2xl font-bold mb-6">KPIs Básicos</h2>

      {/* 🔹 Tarjetas */}
      <div className="grid grid-cols-3 gap-4 mb-8">
        <div className="bg-white shadow rounded-xl p-4 text-center">
          <p className="text-gray-500">Ventas Totales</p>
          <h3 className="text-2xl font-bold text-indigo-600">
            € {kpis.ventas_totales.toLocaleString()}
          </h3>
        </div>
        <div className="bg-white shadow rounded-xl p-4 text-center">
          <p className="text-gray-500">Nº Pedidos</p>
          <h3 className="text-2xl font-bold text-indigo-600">
            {kpis.num_pedidos}
          </h3>
        </div>
        <div className="bg-white shadow rounded-xl p-4 text-center">
          <p className="text-gray-500">Ticket Medio</p>
          <h3 className="text-2xl font-bold text-indigo-600">
            € {kpis.ticket_medio.toFixed(2)}
          </h3>
        </div>
      </div>

      {/* 🔹 Gráfico */}
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
