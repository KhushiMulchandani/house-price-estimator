import { describe, it, expect } from 'vitest';
import { formatINR } from './format';

describe('formatINR', () => {
  it('uses Indian digit grouping with the rupee sign', () => {
    expect(formatINR(8700000)).toBe('₹87,00,000');
  });

  it('rounds to whole rupees', () => {
    expect(formatINR(8689889.57)).toBe('₹86,89,890');
  });
});
