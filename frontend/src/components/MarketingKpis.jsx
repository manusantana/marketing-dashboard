// frontend/src/components/MarketingKpis.jsx
// Displays calculated digital marketing KPIs using temporary mock data.
// TODO: Replace mock data with API call once backend provides metrics.

import { useEffect, useState } from "react";
import { formatNumber } from "../utils/format";
import {
  calculateCTR,
  calculateCPC,
  calculateCPA,
  calculateConversionRate,
  calculateROAS,
} from "../utils/marketing";
import mockMarketingData from "../data/mockMarketing";

export default function MarketingKpis() {
  const [metrics, setMetrics] = useState(null);

  useEffect(() => {
    const { impressions, clicks, conversions, spend, revenue } =
      mockMarketingData;
    setMetrics({
      ctr: calculateCTR(impressions, clicks),
      cpc: calculateCPC(spend, clicks),
      cpa: calculateCPA(spend, conversions),
      conversion_rate: calculateConversionRate(clicks, conversions),
      roas: calculateROAS(revenue, spend),
    });
  }, []);

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
