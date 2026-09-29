import { act, fireEvent, render, screen, waitFor } from '@testing-library/react';
import { MemoryRouter, Route, Routes } from 'react-router-dom';
import { afterEach, beforeEach, describe, expect, it, vi } from 'vitest';
import Register from './Register';

const COLD_START_PATTERN = /backend server is waking up \(Cold Start\)/i;
const SLOW_REQUEST_THRESHOLD_MS = 4000;

const fetchMock = vi.fn();

interface FormValues {
  fullName?: string;
  email?: string;
  password?: string;
}

function renderRegister(): void {
  render(
    <MemoryRouter initialEntries={['/register']}>
      <Routes>
        <Route path="/register" element={<Register />} />
        <Route path="/login" element={<div>Login Page</div>} />
      </Routes>
    </MemoryRouter>,
  );
}

function fillForm({
  fullName = 'Ada Lovelace',
  email = 'ada@example.com',
  password = 'secret123',
}: FormValues = {}): void {
  fireEvent.change(screen.getByPlaceholderText('John Doe'), { target: { value: fullName } });
  fireEvent.change(screen.getByPlaceholderText('you@example.com'), { target: { value: email } });
  fireEvent.change(screen.getByPlaceholderText('At least 6 characters'), {
    target: { value: password },
  });
}

function submit(): void {
  fireEvent.click(screen.getByRole('button', { name: 'Register' }));
}

function jsonResponse(status: number, body: unknown, statusText = ''): Response {
  return {
    ok: status >= 200 && status < 300,
    status,
    statusText,
    json: async () => body,
  } as Response;
}

describe('Register page', () => {
  beforeEach(() => {
    fetchMock.mockReset();
    vi.stubGlobal('fetch', fetchMock);
  });

  afterEach(() => {
    vi.useRealTimers();
    vi.unstubAllGlobals();
  });

  describe('client-side validation', () => {
    it('marks full name, email and password as required', () => {
      renderRegister();

      expect(screen.getByPlaceholderText('John Doe')).toBeRequired();
      expect(screen.getByPlaceholderText('you@example.com')).toBeRequired();
      expect(screen.getByPlaceholderText('At least 6 characters')).toBeRequired();
      expect(screen.getByPlaceholderText('you@example.com')).toHaveAttribute('type', 'email');
    });

    it('rejects passwords shorter than 6 characters without calling the API', () => {
      renderRegister();
      fillForm({ password: '12345' });

      submit();

      expect(screen.getByText(/Password must be at least 6 characters/i)).toBeInTheDocument();
      expect(fetchMock).not.toHaveBeenCalled();
    });

    it('accepts a password of exactly 6 characters', async () => {
      fetchMock.mockResolvedValue(jsonResponse(201, {}));
      renderRegister();
      fillForm({ password: '123456' });

      submit();

      await waitFor(() => expect(fetchMock).toHaveBeenCalledTimes(1));
      expect(screen.queryByText(/Password must be at least 6 characters/i)).not.toBeInTheDocument();
    });

    it('clears a previous validation error on the next valid submit', async () => {
      fetchMock.mockResolvedValue(jsonResponse(201, {}));
      renderRegister();
      fillForm({ password: '123' });
      submit();
      expect(screen.getByText(/Password must be at least 6 characters/i)).toBeInTheDocument();

      fillForm({ password: 'longenough' });
      submit();

      await waitFor(() => expect(screen.getByText('Login Page')).toBeInTheDocument());
    });
  });

  describe('successful registration', () => {
    it('posts the form payload with the selected role and redirects to /login', async () => {
      fetchMock.mockResolvedValue(jsonResponse(201, { id: 7 }));
      renderRegister();
      fillForm();
      fireEvent.click(screen.getByText('I am an instructor'));

      submit();

      await waitFor(() => expect(screen.getByText('Login Page')).toBeInTheDocument());
      const [url, options] = fetchMock.mock.calls[0] as [string, RequestInit];
      expect(url).toBe('/api/v1/auth/register');
      expect(options.method).toBe('POST');
      expect(JSON.parse(options.body as string)).toEqual({
        email: 'ada@example.com',
        full_name: 'Ada Lovelace',
        password: 'secret123',
        role: 'instructor',
      });
    });

    it('defaults the role to student', async () => {
      fetchMock.mockResolvedValue(jsonResponse(201, {}));
      renderRegister();
      fillForm();

      submit();

      await waitFor(() => expect(fetchMock).toHaveBeenCalled());
      const [, options] = fetchMock.mock.calls[0] as [string, RequestInit];
      expect(JSON.parse(options.body as string).role).toBe('student');
    });
  });

  describe('server error handling', () => {
    it('shows the API detail message, e.g. duplicate email', async () => {
      fetchMock.mockResolvedValue(jsonResponse(400, { detail: 'Email already registered' }));
      renderRegister();
      fillForm();

      submit();

      expect(await screen.findByText(/Email already registered/)).toBeInTheDocument();
      expect(screen.queryByText('Login Page')).not.toBeInTheDocument();
    });

    it('falls back to a generic message when the error body has no detail', async () => {
      fetchMock.mockResolvedValue(jsonResponse(422, {}));
      renderRegister();
      fillForm();

      submit();

      expect(await screen.findByText(/Registration failed/)).toBeInTheDocument();
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
      renderRegister();
      fillForm();

      submit();

      expect(
        await screen.findByText(/Server error: 500 Internal Server Error/),
      ).toBeInTheDocument();
    });

    it.each([502, 503, 504])('shows the cold-start message on gateway status %i', async (status) => {
      fetchMock.mockResolvedValue(jsonResponse(status, {}));
      renderRegister();
      fillForm();

      submit();

      expect(await screen.findByText(COLD_START_PATTERN)).toBeInTheDocument();
    });

    it('shows a network error message when fetch rejects with a TypeError', async () => {
      fetchMock.mockRejectedValue(new TypeError('Failed to fetch'));
      renderRegister();
      fillForm();

      submit();

      expect(await screen.findByText(/Network request failed/i)).toBeInTheDocument();
      expect(screen.getByRole('button', { name: 'Register' })).toBeEnabled();
    });
  });

  describe('slow request (cold start) feedback', () => {
    it('disables the button and warns about cold start after 4s without a response', () => {
      vi.useFakeTimers();
      fetchMock.mockReturnValue(new Promise<Response>(() => {}));
      renderRegister();
      fillForm();

      submit();

      const button = screen.getByRole('button', { name: 'Registering...' });
      expect(button).toBeDisabled();
      expect(screen.queryByText(COLD_START_PATTERN)).not.toBeInTheDocument();

      act(() => {
        vi.advanceTimersByTime(SLOW_REQUEST_THRESHOLD_MS);
      });

      expect(screen.getByText(COLD_START_PATTERN)).toBeInTheDocument();
    });
  });
});
