// frontend/src/utils/marketing.js
// Helper functions to calculate common digital marketing metrics.
// Each function handles divide-by-zero safely and returns a number.

/**
 * Click-through rate (CTR)
 * @param {number} impressions - Number of ad impressions.
 * @param {number} clicks - Number of clicks.
 * @returns {number} CTR as a fraction (0-1).
 */
export function calculateCTR(impressions, clicks) {
  if (!impressions) return 0;
  return clicks / impressions;
}

/**
 * Cost per click (CPC)
 * @param {number} spend - Total advertising spend.
 * @param {number} clicks - Number of clicks.
 * @returns {number} Cost per click.
 */
export function calculateCPC(spend, clicks) {
  if (!clicks) return 0;
  return spend / clicks;
}

/**
 * Cost per acquisition (CPA)
 * @param {number} spend - Total advertising spend.
 * @param {number} conversions - Number of conversions.
 * @returns {number} Cost per acquisition.
 */
export function calculateCPA(spend, conversions) {
  if (!conversions) return 0;
  return spend / conversions;
}

/**
 * Conversion rate (CVR)
 * @param {number} clicks - Number of clicks.
 * @param {number} conversions - Number of conversions.
 * @returns {number} Conversion rate as a fraction (0-1).
 */
export function calculateConversionRate(clicks, conversions) {
  if (!clicks) return 0;
  return conversions / clicks;
}

/**
 * Return on ad spend (ROAS)
 * @param {number} revenue - Revenue generated from ads.
 * @param {number} spend - Total advertising spend.
 * @returns {number} ROAS ratio.
 */
export function calculateROAS(revenue, spend) {
  if (!spend) return 0;
  return revenue / spend;
}

