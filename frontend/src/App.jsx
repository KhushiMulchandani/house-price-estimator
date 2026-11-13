import { useState } from 'react';
import { estimatePrice } from './api';
import PriceEstimatorForm from './components/PriceEstimatorForm';
import ResultBox from './components/ResultBox';
import ErrorMessage from './components/ErrorMessage';

// Turn an axios error into { message, fieldErrors } for the UI.
function describeError(err) {
  const res = err.response;
  if (!res) {
    return { message: 'Could not reach the server. Is the backend running?', fieldErrors: {} };
  }
  const data = res.data;
  if (data && typeof data.detail === 'string') {
    return { message: data.detail, fieldErrors: {} };
  }
  if (res.status === 400 && data && typeof data === 'object') {
    return { message: 'Please fix the highlighted fields.', fieldErrors: data };
  }
  return { message: 'Something went wrong. Please try again.', fieldErrors: {} };
}

export default function App() {
  const [loading, setLoading] = useState(false);
  const [price, setPrice] = useState(null);
  const [message, setMessage] = useState('');
  const [serverErrors, setServerErrors] = useState({});

  const handleSubmit = async (payload) => {
    setLoading(true);
    setPrice(null); // old result clears while loading
    setMessage('');
    setServerErrors({});
    try {
      const data = await estimatePrice(payload);
      setPrice(data.estimated_price);
    } catch (err) {
      const { message: msg, fieldErrors } = describeError(err);
      setMessage(msg);
      setServerErrors(fieldErrors);
    } finally {
      setLoading(false);
    }
  };

  return (
    <main className="card">
      <h1>House Price Estimator</h1>
      <p className="subtitle">Enter the details to get an estimated price.</p>
      <PriceEstimatorForm onSubmit={handleSubmit} loading={loading} serverErrors={serverErrors} />
      <ErrorMessage message={message} />
      {loading && (
      <p className="hint">The first request after a quiet period can take up to a minute while the server wakes up.</p>
      )}
      <ResultBox price={price} />
    </main>
  );
}
