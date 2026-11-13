import { render, screen, fireEvent } from '@testing-library/react';
import { describe, it, expect, vi, beforeEach } from 'vitest';
import App from './App';
import { estimatePrice } from './api';

vi.mock('./api', () => ({ estimatePrice: vi.fn() }));

const VALID = { sqft: '1500', bedrooms: '3', age: '10', location_rating: '4' };

function fill(values = VALID) {
  fireEvent.change(screen.getByLabelText(/square footage/i), { target: { value: values.sqft } });
  fireEvent.change(screen.getByLabelText(/bedrooms/i), { target: { value: values.bedrooms } });
  fireEvent.change(screen.getByLabelText(/house age/i), { target: { value: values.age } });
  fireEvent.change(screen.getByLabelText(/location rating/i), { target: { value: values.location_rating } });
}

function submit() {
  fireEvent.click(screen.getByRole('button', { name: /estimate price|estimating/i }));
}

describe('App', () => {
  beforeEach(() => {
    estimatePrice.mockReset();
  });

  it('renders four labelled inputs and no result at first', () => {
    render(<App />);
    expect(screen.getByLabelText(/square footage/i)).toBeInTheDocument();
    expect(screen.getByLabelText(/bedrooms/i)).toBeInTheDocument();
    expect(screen.getByLabelText(/house age/i)).toBeInTheDocument();
    expect(screen.getByLabelText(/location rating/i)).toBeInTheDocument();
    expect(screen.queryByRole('status')).not.toBeInTheDocument();
  });

  it('submits numbers once and shows the price in INR', async () => {
    estimatePrice.mockResolvedValue({ estimated_price: 8700000 });
    render(<App />);
    fill();
    submit();
    expect(await screen.findByText('₹87,00,000')).toBeInTheDocument();
    expect(estimatePrice).toHaveBeenCalledTimes(1);
    expect(estimatePrice).toHaveBeenCalledWith({
      sqft: 1500,
      bedrooms: 3,
      age: 10,
      location_rating: 4,
    });
  });

  it('blocks submit and shows a hint when a value is out of range', async () => {
    render(<App />);
    fill({ ...VALID, sqft: '5' });
    submit();
    expect(await screen.findByText(/must be between 300 and 10000/i)).toBeInTheDocument();
    expect(estimatePrice).not.toHaveBeenCalled();
  });

  it('shows field errors returned by the API (400)', async () => {
    estimatePrice.mockRejectedValue(
      Object.assign(new Error('Bad Request'), {
        response: { status: 400, data: { sqft: ['Ensure this value is greater than or equal to 300.'] } },
      }),
    );
    render(<App />);
    fill();
    submit();
    expect(await screen.findByText(/ensure this value is greater than or equal to 300/i)).toBeInTheDocument();
  });

  it('shows a connection message when the server is unreachable', async () => {
    estimatePrice.mockRejectedValue(new Error('Network Error'));
    render(<App />);
    fill();
    submit();
    expect(await screen.findByText(/could not reach the server/i)).toBeInTheDocument();
  });

  it('disables the button while the request is pending', () => {
    estimatePrice.mockReturnValue(new Promise(() => {})); // never resolves
    render(<App />);
    fill();
    submit();
    expect(screen.getByRole('button', { name: /estimating/i })).toBeDisabled();
  });
});
