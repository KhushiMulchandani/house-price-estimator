// 8689889.57 -> "₹86,89,890" (Indian digit grouping)
const inr = new Intl.NumberFormat('en-IN', {
  style: 'currency',
  currency: 'INR',
  maximumFractionDigits: 0,
});

export function formatINR(value) {
  return inr.format(value);
}
