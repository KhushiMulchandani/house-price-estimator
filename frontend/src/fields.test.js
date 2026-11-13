import { describe, it, expect } from 'vitest';
import { validate, toPayload } from './fields';

const valid = { sqft: '1500', bedrooms: '3', age: '10', location_rating: '4' };

describe('validate', () => {
  it('accepts valid values', () => {
    expect(validate(valid)).toEqual({});
  });

  it('accepts boundary values', () => {
    expect(validate({ sqft: '300', bedrooms: '1', age: '0', location_rating: '1' })).toEqual({});
    expect(validate({ sqft: '10000', bedrooms: '10', age: '100', location_rating: '5' })).toEqual({});
  });

  it('requires every field', () => {
    const errors = validate({ sqft: '', bedrooms: '', age: '', location_rating: '' });
    expect(Object.keys(errors)).toHaveLength(4);
  });

  it('rejects out-of-range values', () => {
    expect(validate({ ...valid, sqft: '299' }).sqft).toMatch(/between 300 and 10000/);
    expect(validate({ ...valid, location_rating: '6' }).location_rating).toBeDefined();
    expect(validate({ ...valid, age: '-1' }).age).toBeDefined();
  });

  it('rejects non-integers for bedrooms and rating', () => {
    expect(validate({ ...valid, bedrooms: '2.5' }).bedrooms).toMatch(/whole number/);
  });

  it('rejects non-numeric text', () => {
    expect(validate({ ...valid, sqft: 'abc' }).sqft).toBeDefined();
  });
});

describe('toPayload', () => {
  it('converts strings to numbers', () => {
    expect(toPayload(valid)).toEqual({ sqft: 1500, bedrooms: 3, age: 10, location_rating: 4 });
  });
});
