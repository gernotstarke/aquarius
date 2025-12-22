import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import { describe, it, expect, vi, beforeEach } from 'vitest';
import { BrowserRouter } from 'react-router-dom';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import WettkampfForm from '../WettkampfForm';

// Mock the API client
vi.mock('../../api/client', () => ({
  default: {
    get: vi.fn().mockImplementation((url) => {
        if (url === '/saison') return Promise.resolve({ data: [] });
        if (url === '/schwimmbad') return Promise.resolve({ data: [] });
        return Promise.resolve({ data: {} });
    }),
    post: vi.fn(),
    put: vi.fn(),
  },
}));

const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      retry: false,
    },
  },
});

const renderWithProviders = (ui: React.ReactElement) => {
  return render(
    <QueryClientProvider client={queryClient}>
      <BrowserRouter>{ui}</BrowserRouter>
    </QueryClientProvider>
  );
};

describe('WettkampfForm Business Rules', () => {
  beforeEach(() => {
    vi.clearAllMocks();
  });

  it('should show error and wobble when max_teilnehmer is <= 1', async () => {
    renderWithProviders(<WettkampfForm />);
    
    const input = screen.getByLabelText(/Max. Teilnehmer/i);
    const submitBtn = screen.getByRole('button', { name: /Erstellen/i });

    // Set invalid value
    fireEvent.change(input, { target: { value: '1' } });
    fireEvent.click(submitBtn);

    // Check for error message
    expect(await screen.findByText(/Max. Teilnehmer muss größer als 1 sein/i)).toBeInTheDocument();
    
    // Check if parent container has wobble class (via class search)
    const errorMsg = screen.getByText(/Max. Teilnehmer muss größer als 1 sein/i);
    const formGroup = errorMsg.closest('.animate-wobble');
    expect(formGroup).not.toBeNull();
  });

  it('should not show error when max_teilnehmer is > 1', async () => {
    renderWithProviders(<WettkampfForm />);
    
    const input = screen.getByLabelText(/Max. Teilnehmer/i);
    const submitBtn = screen.getByRole('button', { name: /Erstellen/i });

    // Set valid value
    fireEvent.change(input, { target: { value: '10' } });
    fireEvent.click(submitBtn);

    // Error should NOT be there
    const errorMsg = screen.queryByText(/Max. Teilnehmer muss größer als 1 sein/i);
    expect(errorMsg).toBeNull();
  });
});
