import axios from 'axios';

const client = axios.create({
  baseURL: import.meta.env.VITE_API_URL ?? 'http://localhost:8000',
  timeout: 60000,
});

// payload: { sqft, bedrooms, age, location_rating } as numbers
// resolves to { estimated_price }
export async function estimatePrice(payload) {
  const { data } = await client.post('/api/v1/estimate/', payload);
  return data;
}
