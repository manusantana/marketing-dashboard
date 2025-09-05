// frontend/src/utils/format.js
// Utility functions for consistent number formatting in Spanish locale.
// Ensures thousands are separated with dots and decimals with commas.
// The `decimals` parameter controls the number of decimal places displayed.
export function formatNumber(value, decimals = 2) {
  return value.toLocaleString("es-ES", {
    minimumFractionDigits: decimals,
    maximumFractionDigits: decimals,
  });
}
