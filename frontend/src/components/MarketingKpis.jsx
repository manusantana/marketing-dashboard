// frontend/src/components/MarketingKpis.jsx
// Displays calculated digital marketing KPIs using data from the backend.
import { useEffect, useState } from "react";
import client from "../api/client";
import { formatNumber } from "../utils/format";
import {
  calculateCTR,
  calculateCPC,
  calculateCPA,
  calculateConversionRate,
  calculateROAS,
} from "../utils/marketing";

export default function MarketingKpis() {
  const [metrics, setMetrics] = useState(null);
  const [error, setError] = useState("");

  const fetchMetrics = async () => {
    try {
      const res = await client.get("/kpis/marketing");
      const raw = res.data;
      setMetrics({
        ctr: calculateCTR(raw.impressions, raw.clicks),
        cpc: calculateCPC(raw.spend, raw.clicks),
        cpa: calculateCPA(raw.spend, raw.conversions),
        conversion_rate: calculateConversionRate(
          raw.clicks,
          raw.conversions
        ),
        roas: calculateROAS(raw.revenue, raw.spend),
      });
    } catch (err) {
      console.error("❌ Error cargando KPIs de marketing:", err);
      setError("No se pudieron cargar los KPIs de marketing");
    }
  };

  useEffect(() => {
    fetchMetrics();
  }, []);

  if (error) return <p className="p-4 text-red-600">{error}</p>;
  if (!metrics) return <p className="p-4">Cargando KPIs de marketing...</p>;

  return (
    <section className="mt-10">
      <h2 className="text-2xl font-bold mb-6">KPIs de Marketing</h2>
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        <div className="card text-center">
          <p className="text-gray-500">CTR</p>
          <h3 className="text-2xl font-bold text-primary">
            {formatNumber(metrics.ctr * 100)}%
          </h3>
        </div>
        <div className="card text-center">
          <p className="text-gray-500">CPC</p>
          <h3 className="text-2xl font-bold text-primary">
            €{formatNumber(metrics.cpc)}
          </h3>
        </div>
        <div className="card text-center">
          <p className="text-gray-500">CPA</p>
          <h3 className="text-2xl font-bold text-primary">
            €{formatNumber(metrics.cpa)}
          </h3>
        </div>
        <div className="card text-center">
          <p className="text-gray-500">Tasa de conversión</p>
          <h3 className="text-2xl font-bold text-primary">
            {formatNumber(metrics.conversion_rate * 100)}%
          </h3>
        </div>
        <div className="card text-center">
          <p className="text-gray-500">ROAS</p>
          <h3 className="text-2xl font-bold text-primary">
            {formatNumber(metrics.roas)}
          </h3>
        </div>
      </div>
    </section>
  );
}

