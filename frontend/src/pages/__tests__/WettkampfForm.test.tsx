import { render, screen, act } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { describe, it, expect, vi, beforeEach, afterEach } from 'vitest';
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
      <BrowserRouter future={{ v7_startTransition: true, v7_relativeSplatPath: true }}>
        {ui}
      </BrowserRouter>
    </QueryClientProvider>
  );
};

describe('WettkampfForm Business Rules', () => {
  beforeEach(() => {
    vi.clearAllMocks();
    queryClient.clear();
    vi.useFakeTimers();
  });

  afterEach(() => {
    vi.runOnlyPendingTimers();
    vi.useRealTimers();
  });

  it('should show error and wobble when max_teilnehmer is <= 1', async () => {
    const user = userEvent.setup({ advanceTimers: vi.advanceTimersByTime });
    renderWithProviders(<WettkampfForm />);
    
    // Fill required fields
    await user.type(screen.getByLabelText(/Name/i), 'Test Wettkampf');
    await user.type(screen.getByLabelText(/Datum/i), '2024-12-24');
    
    const input = screen.getByLabelText(/Max. Teilnehmer/i);
    const submitBtn = screen.getByRole('button', { name: /Erstellen/i });

    // Set invalid value
    await user.clear(input);
    await user.type(input, '1');
    
    await user.click(submitBtn);

    // Wait for the error message
    // Note: findBy uses waitFor internally, which advances fake timers if configured
    const errorMsg = await screen.findByText(/muss größer als 1 sein/i);
    expect(errorMsg).toBeInTheDocument();
    
    // Check if parent container has wobble class
    const wobbleContainer = errorMsg.closest('.animate-wobble');
    expect(wobbleContainer).not.toBeNull();

    // Fast-forward time to handle the wobble timeout (500ms)
    // Wrapping in act because this triggers a state update (setIsWobbling(false))
    act(() => {
        vi.advanceTimersByTime(500);
    });
  });

  it('should not show error when max_teilnehmer is > 1', async () => {
    const user = userEvent.setup({ advanceTimers: vi.advanceTimersByTime });
    renderWithProviders(<WettkampfForm />);
    
    const input = screen.getByLabelText(/Max. Teilnehmer/i);
    const submitBtn = screen.getByRole('button', { name: /Erstellen/i });

    // Set valid value
    await user.type(input, '10');
    await user.click(submitBtn);

    // Error should NOT be there
    const errorMsg = screen.queryByText(/größer als 1 sein/i);
    expect(errorMsg).toBeNull();
  });
});
