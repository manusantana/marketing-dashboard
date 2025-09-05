// frontend/src/pages/Dashboard.jsx
import { useEffect, useState } from "react";
import client from "../api/client";
import { BarChart, Bar, XAxis, YAxis, Tooltip, Legend, ResponsiveContainer } from "recharts";
import Upload from "../components/Upload"; // ← ruta corregida

export default function Dashboard() {
  const [kpis, setKpis] = useState(null);
  const [error, setError] = useState("");

  useEffect(() => {
    const fetchKpis = async () => {
      try {
        const res = await client.get("/kpis/basic");
        setKpis({
          ventas_totales: res.data.turnover ?? 0,
          num_pedidos: res.data.orders ?? 0,
          ticket_medio: res.data.ticket_average ?? 0,
          margen: res.data.margin ?? 0,
          descuento: res.data.discount ?? 0,
        });
      } catch (err) {
        console.error("❌ Error cargando KPIs:", err);
        setError("No se pudieron cargar los KPIs");
      }
    };
    fetchKpis();
  }, []);

  if (error)
    return <p className="p-4 text-red-600">{error}</p>;
  if (!kpis) return <p className="p-4">Cargando KPIs...</p>;

  const data = [
    { name: "Ventas Totales", value: kpis.ventas_totales },
    { name: "Ticket Medio", value: kpis.ticket_medio },
  ];

  return (
    <div className="p-6 space-y-10">
      <section>
        <h2 className="text-2xl font-bold mb-6">KPIs Básicos</h2>

        {/* Tarjetas */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-8">
          <div className="card text-center">
            <p className="text-gray-500">Ventas Totales</p>

            <h3 className="text-2xl font-bold text-indigo-600">
              €
              {kpis.ventas_totales.toLocaleString(undefined, {
                minimumFractionDigits: 2,
                maximumFractionDigits: 2,
              })}
            </h3>
          </div>
          <div className="card text-center">
            <p className="text-gray-500">Nº Pedidos</p>
            <h3 className="text-2xl font-bold text-primary">
              {kpis.num_pedidos}
            </h3>
          </div>
          <div className="card text-center">
            <p className="text-gray-500">Ticket Medio</p>
            <h3 className="text-2xl font-bold text-primary">
              € {kpis.ticket_medio.toFixed(2)}
            </h3>
          </div>
          <div className="bg-white shadow rounded-xl p-4 text-center">
            <p className="text-gray-500">Margen</p>
            <h3 className="text-2xl font-bold text-indigo-600">
              € {kpis.margen.toFixed(2)}
            </h3>
          </div>
          <div className="bg-white shadow rounded-xl p-4 text-center">
            <p className="text-gray-500">Descuento</p>
            <h3 className="text-2xl font-bold text-indigo-600">
              € {kpis.descuento.toFixed(2)}
            </h3>
          </div>
        </div>

        {/* Gráfico */}
        <ResponsiveContainer width="100%" height={300}>
          <BarChart data={data}>
            <XAxis dataKey="name" />
            <YAxis />
            <Tooltip />
            <Legend />
            <Bar dataKey="value" fill="#6366F1" />
          </BarChart>
        </ResponsiveContainer>
      </section>

      {/* Sección de Upload */}
      <section>
        <h2 className="text-2xl font-bold mb-4">Carga de datos</h2>
        <div className="card">
          <Upload />
        </div>
      </section>
    </div>
  );
}
