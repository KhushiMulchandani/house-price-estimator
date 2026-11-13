import { useState } from 'react';
import { FIELDS, EMPTY_VALUES, validate, toPayload } from '../fields';

export default function PriceEstimatorForm({ onSubmit, loading = false, serverErrors = {} }) {
  // One state object for all four inputs (strings, as typed).
  const [values, setValues] = useState(EMPTY_VALUES);
  const [errors, setErrors] = useState({});

  const handleChange = (e) => {
    const { name, value } = e.target;
    setValues((prev) => ({ ...prev, [name]: value }));
    if (errors[name]) {
      setErrors((prev) => {
        const next = { ...prev };
        delete next[name];
        return next;
      });
    }
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    if (loading) return;
    const found = validate(values);
    setErrors(found);
    if (Object.keys(found).length > 0) return; // block submit, show hints
    onSubmit(toPayload(values));
  };

  return (
    <form onSubmit={handleSubmit} noValidate>
      {FIELDS.map((f) => {
        const error = errors[f.name] ?? serverErrors[f.name]?.[0];
        const hintId = `${f.name}-hint`;
        const errorId = `${f.name}-error`;
        return (
          <div className="field" key={f.name}>
            <label htmlFor={f.name}>{f.label}</label>
            <input
              id={f.name}
              name={f.name}
              type="number"
              inputMode={f.integer ? 'numeric' : 'decimal'}
              min={f.min}
              max={f.max}
              step={f.integer ? 1 : 'any'}
              placeholder={f.placeholder}
              value={values[f.name]}
              onChange={handleChange}
              aria-invalid={Boolean(error)}
              aria-describedby={error ? `${hintId} ${errorId}` : hintId}
            />
            <p id={hintId} className="hint">
              Between {f.min} and {f.max}
            </p>
            {error && (
              <p id={errorId} className="field-error" role="alert">
                {error}
              </p>
            )}
          </div>
        );
      })}
      <button type="submit" disabled={loading}>
        {loading ? 'Estimating...' : 'Estimate Price'}
      </button>
    </form>
  );
}
