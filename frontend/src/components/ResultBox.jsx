import { formatINR } from '../utils/format';

export default function ResultBox({ price }) {
  if (price === null || price === undefined) return null;
  return (
    <section className="result" role="status">
      <h2>Estimated price</h2>
      <p className="price">{formatINR(price)}</p>
      <p className="disclaimer">
        Demo estimate based on synthetic data. Not a real market valuation.
      </p>
    </section>
  );
}
