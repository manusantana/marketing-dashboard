// frontend/src/pages/Dashboard.jsx
import { useEffect, useState } from "react";
import client from "../api/client";
import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  Tooltip,
  Legend,
  ResponsiveContainer,
  LabelList,
} from "recharts";

export default function Dashboard() {
  const [kpis, setKpis] = useState(null);

  useEffect(() => {
    const fetchKpis = async () => {
      try {
        const res = await client.get("/kpis/basic");
        setKpis({
          ventas_totales: res.data.turnover ?? 0,
          num_pedidos: res.data.orders ?? 0,
          ticket_medio:
            res.data.turnover && res.data.orders
              ? res.data.turnover / res.data.orders
              : 0,
          margen: res.data.margin ?? 0,
        });
      } catch (err) {
        console.error("❌ Error cargando KPIs:", err);
      }
    };
    fetchKpis();
  }, []);

  if (!kpis) return <p className="p-4">Cargando KPIs...</p>;

  const data = [
    { name: "Ventas Totales", value: kpis.ventas_totales },
    { name: "Ticket Medio", value: kpis.ticket_medio },
  ];

  return (
    <div className="p-6 space-y-10">
      <section>
        <h2 className="text-2xl font-bold mb-6">KPIs Básicos</h2>

      {/* 🔹 Fila de indicadores */}
      <div className="overflow-x-auto mb-8">
        <table className="min-w-full text-center">
          <thead className="bg-indigo-100">
            <tr>
              <th className="p-2">Ventas Totales</th>
              <th className="p-2">Nº Pedidos</th>
              <th className="p-2">Ticket Medio</th>
            </tr>
          </thead>
          <tbody>
            <tr>
              <td className="p-2">€ {kpis.ventas_totales.toLocaleString()}</td>
              <td className="p-2">{kpis.num_pedidos}</td>
              <td className="p-2">€ {kpis.ticket_medio.toFixed(2)}</td>
            </tr>
          </tbody>
        </table>
      </div>

      {/* 🔹 Gráfico */}
      <ResponsiveContainer width="100%" height={300}>
        <BarChart data={data}>
          <XAxis dataKey="name" />
          <YAxis />
          <Tooltip />
          <Legend />
          <Bar dataKey="value" fill="#6366F1">
            <LabelList dataKey="value" position="top" />
          </Bar>
        </BarChart>
      </ResponsiveContainer>
    </div>
  );
}
