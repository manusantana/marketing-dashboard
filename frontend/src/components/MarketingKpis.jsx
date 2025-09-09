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

  const sampleMetrics = () => {
    const impressions = 10_000 + Math.floor(Math.random() * 20_000);
    const clicks = Math.floor(impressions * (0.02 + Math.random() * 0.08));
    const conversions = Math.max(
      1,
      Math.floor(clicks * (0.05 + Math.random() * 0.2))
    );
    const spend = 500 + Math.random() * 4_500;
    const revenue = spend * (1 + Math.random() * 4);
    return { impressions, clicks, conversions, spend, revenue };
  };

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
      setError("Mostrando datos de ejemplo");
      const fallback = sampleMetrics();
      setMetrics({
        ctr: calculateCTR(fallback.impressions, fallback.clicks),
        cpc: calculateCPC(fallback.spend, fallback.clicks),
        cpa: calculateCPA(fallback.spend, fallback.conversions),
        conversion_rate: calculateConversionRate(
          fallback.clicks,
          fallback.conversions
        ),
        roas: calculateROAS(fallback.revenue, fallback.spend),
      });
    }
  };

  useEffect(() => {
    fetchMetrics();
  }, []);

  if (!metrics) return <p className="p-4">Cargando KPIs de marketing...</p>;

  return (
    <section className="mt-10">
      <h2 className="text-2xl font-bold mb-6">KPIs de Marketing</h2>
      {error && <p className="mb-4 text-yellow-600">{error}</p>}
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

