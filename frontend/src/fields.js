// Single source of truth for the form fields.
// Ranges come from docs/02-srs.md and must match the backend serializer.
export const FIELDS = [
  { name: 'sqft', label: 'Square footage (sq ft)', placeholder: 'e.g. 1500', min: 300, max: 10000, integer: false },
  { name: 'bedrooms', label: 'Bedrooms', placeholder: 'e.g. 3', min: 1, max: 10, integer: true },
  { name: 'age', label: 'House age (years)', placeholder: 'e.g. 10', min: 0, max: 100, integer: false },
  { name: 'location_rating', label: 'Location rating', placeholder: '1 (poor) to 5 (excellent)', min: 1, max: 5, integer: true },
];

export const EMPTY_VALUES = Object.fromEntries(FIELDS.map((f) => [f.name, '']));

// Returns { fieldName: "message" } for every invalid field ({} means valid).
export function validate(values) {
  const errors = {};
  for (const f of FIELDS) {
    const raw = String(values[f.name] ?? '').trim();
    if (raw === '') {
      errors[f.name] = 'This field is required.';
      continue;
    }
    const num = Number(raw);
    if (!Number.isFinite(num)) {
      errors[f.name] = 'Enter a valid number.';
    } else if (f.integer && !Number.isInteger(num)) {
      errors[f.name] = 'Enter a whole number.';
    } else if (num < f.min || num > f.max) {
      errors[f.name] = `Must be between ${f.min} and ${f.max}.`;
    }
  }
  return errors;
}

// The API expects numbers, not strings.
export function toPayload(values) {
  return Object.fromEntries(FIELDS.map((f) => [f.name, Number(values[f.name])]));
}
