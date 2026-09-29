import { act, fireEvent, render, screen, waitFor } from '@testing-library/react';
import { MemoryRouter, Route, Routes } from 'react-router-dom';
import { afterEach, beforeEach, describe, expect, it, vi } from 'vitest';
import Login from './Login';
import { useAuth } from '../context/AuthContext';

vi.mock('../context/AuthContext', () => ({
  useAuth: vi.fn(),
}));

const COLD_START_PATTERN = /backend server is waking up \(Cold Start\)/i;
const SLOW_REQUEST_THRESHOLD_MS = 4000;

const fetchMock = vi.fn();
const checkAuthMock = vi.fn();

function renderLogin(): void {
  render(
    <MemoryRouter initialEntries={['/login']}>
      <Routes>
        <Route path="/login" element={<Login />} />
        <Route path="/student" element={<div>Student Home</div>} />
        <Route path="/instructor" element={<div>Instructor Home</div>} />
        <Route path="/" element={<div>Landing Page</div>} />
      </Routes>
    </MemoryRouter>,
  );
}

function fillAndSubmit(email = 'ada@example.com', password = 'secret123'): void {
  fireEvent.change(screen.getByPlaceholderText('you@example.com'), { target: { value: email } });
  fireEvent.change(screen.getByPlaceholderText('••••••••'), { target: { value: password } });
  fireEvent.click(screen.getByRole('button', { name: 'Login' }));
}

function jsonResponse(status: number, body: unknown, statusText = ''): Response {
  return {
    ok: status >= 200 && status < 300,
    status,
    statusText,
    json: async () => body,
  } as Response;
}

describe('Login page', () => {
  beforeEach(() => {
    fetchMock.mockReset();
    checkAuthMock.mockReset().mockResolvedValue(undefined);
    vi.stubGlobal('fetch', fetchMock);
    vi.mocked(useAuth).mockReturnValue({
      user: null,
      isAuthenticated: false,
      isLoading: false,
      login: vi.fn(),
      logout: vi.fn(),
      checkAuth: checkAuthMock,
    });
  });

  afterEach(() => {
    vi.useRealTimers();
    vi.unstubAllGlobals();
  });

  describe('slow request (cold start) feedback', () => {
    it('shows a loading button immediately and a cold-start hint after 4s', () => {
      vi.useFakeTimers();
      fetchMock.mockReturnValue(new Promise<Response>(() => {}));
      renderLogin();

      fillAndSubmit();

      expect(screen.getByRole('button', { name: 'Logging in...' })).toBeDisabled();

      act(() => {
        vi.advanceTimersByTime(SLOW_REQUEST_THRESHOLD_MS - 1);
      });
      expect(screen.queryByText(COLD_START_PATTERN)).not.toBeInTheDocument();

      act(() => {
        vi.advanceTimersByTime(1);
      });
      expect(screen.getByText(COLD_START_PATTERN)).toBeInTheDocument();
    });

    it('does not show the cold-start hint when the server answers quickly', async () => {
      vi.useFakeTimers();
      fetchMock.mockResolvedValue(jsonResponse(401, { detail: 'Incorrect email or password' }));
      renderLogin();

      fillAndSubmit();
      await act(async () => {
        await vi.runAllTimersAsync();
      });

      expect(screen.getByText(/Incorrect email or password/)).toBeInTheDocument();
      expect(screen.queryByText(COLD_START_PATTERN)).not.toBeInTheDocument();
    });

    it('replaces the cold-start hint with the real result once the slow request fails', async () => {
      vi.useFakeTimers();
      let resolveFetch: (res: Response) => void = () => {};
      fetchMock.mockReturnValue(
        new Promise<Response>((resolve) => {
          resolveFetch = resolve;
        }),
      );
      renderLogin();
      fillAndSubmit();

      act(() => {
        vi.advanceTimersByTime(SLOW_REQUEST_THRESHOLD_MS);
      });
      expect(screen.getByText(COLD_START_PATTERN)).toBeInTheDocument();

      await act(async () => {
        resolveFetch(jsonResponse(401, { detail: 'Incorrect email or password' }));
      });

      expect(screen.getByText(/Incorrect email or password/)).toBeInTheDocument();
      expect(screen.queryByText(COLD_START_PATTERN)).not.toBeInTheDocument();
      expect(screen.getByRole('button', { name: 'Login' })).toBeEnabled();
    });
  });

  describe('error messages', () => {
    it('shows the API detail for invalid credentials', async () => {
      fetchMock.mockResolvedValue(jsonResponse(401, { detail: 'Incorrect email or password' }));
      renderLogin();

      fillAndSubmit();

      expect(await screen.findByText(/Incorrect email or password/)).toBeInTheDocument();
      expect(checkAuthMock).not.toHaveBeenCalled();
    });

    it('falls back to "Login failed" when the error body has no detail', async () => {
      fetchMock.mockResolvedValue(jsonResponse(400, {}));
      renderLogin();

      fillAndSubmit();

      expect(await screen.findByText(/Login failed/)).toBeInTheDocument();
    });

    it('shows the HTTP status when the error body is not JSON', async () => {
      fetchMock.mockResolvedValue({
        ok: false,
        status: 500,
        statusText: 'Internal Server Error',
        json: async () => {
          throw new SyntaxError('Unexpected token <');
        },
      } as unknown as Response);
      renderLogin();

      fillAndSubmit();

      expect(
        await screen.findByText(/Server error: 500 Internal Server Error/),
      ).toBeInTheDocument();
    });

    it.each([502, 503, 504])('shows the cold-start message on gateway status %i', async (status) => {
      fetchMock.mockResolvedValue(jsonResponse(status, {}));
      renderLogin();

      fillAndSubmit();

      expect(await screen.findByText(COLD_START_PATTERN)).toBeInTheDocument();
    });

    it('shows a network error message when fetch rejects with a TypeError', async () => {
      fetchMock.mockRejectedValue(new TypeError('Failed to fetch'));
      renderLogin();

      fillAndSubmit();

      expect(await screen.findByText(/Network request failed/i)).toBeInTheDocument();
      expect(screen.getByRole('button', { name: 'Login' })).toBeEnabled();
    });

    it('clears the previous error when the user retries', async () => {
      fetchMock
        .mockResolvedValueOnce(jsonResponse(401, { detail: 'Incorrect email or password' }))
        .mockReturnValueOnce(new Promise<Response>(() => {}));
      renderLogin();

      fillAndSubmit();
      expect(await screen.findByText(/Incorrect email or password/)).toBeInTheDocument();

      fillAndSubmit();

      expect(screen.queryByText(/Incorrect email or password/)).not.toBeInTheDocument();
    });
  });

  describe('successful login', () => {
    it('sends credentials with cookies and redirects a student to /student', async () => {
      fetchMock.mockResolvedValue(jsonResponse(200, { role: 'student' }));
      renderLogin();

      fillAndSubmit();

      await waitFor(() => expect(screen.getByText('Student Home')).toBeInTheDocument());
      const [url, options] = fetchMock.mock.calls[0] as [string, RequestInit];
      expect(url).toBe('/api/v1/auth/login');
      expect(options.credentials).toBe('include');
      expect(JSON.parse(options.body as string)).toEqual({
        email: 'ada@example.com',
        password: 'secret123',
      });
      expect(checkAuthMock).toHaveBeenCalledTimes(1);
    });

    it('redirects an instructor to /instructor', async () => {
      fetchMock.mockResolvedValue(jsonResponse(200, { role: 'instructor' }));
      renderLogin();

      fillAndSubmit();

      await waitFor(() => expect(screen.getByText('Instructor Home')).toBeInTheDocument());
    });
  });
});
