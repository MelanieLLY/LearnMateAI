import { render, screen } from '@testing-library/react';
import { MemoryRouter, Route, Routes } from 'react-router-dom';
import { beforeEach, describe, expect, it, vi } from 'vitest';
import ProtectedRoute from './ProtectedRoute';
import { useAuth } from '../context/AuthContext';
import type { User } from '../context/AuthContext';

vi.mock('../context/AuthContext', () => ({
  useAuth: vi.fn(),
}));

type AuthState = ReturnType<typeof useAuth>;

const mockedUseAuth = vi.mocked(useAuth);

function makeUser(role: User['role']): User {
  return { id: 1, email: `${role}@example.com`, role, created_at: '2026-01-01T00:00:00Z' };
}

function mockAuth(overrides: Partial<AuthState>): void {
  mockedUseAuth.mockReturnValue({
    user: null,
    isAuthenticated: false,
    isLoading: false,
    login: vi.fn(),
    logout: vi.fn(),
    checkAuth: vi.fn(),
    ...overrides,
  });
}

function renderAt(path: string, allowedRoles?: User['role'][]): void {
  render(
    <MemoryRouter initialEntries={[path]}>
      <Routes>
        <Route
          path="/instructor"
          element={
            <ProtectedRoute allowedRoles={allowedRoles}>
              <div>Instructor Area</div>
            </ProtectedRoute>
          }
        />
        <Route path="/login" element={<div>Login Page</div>} />
        <Route path="/404" element={<div>Not Found Page</div>} />
      </Routes>
    </MemoryRouter>,
  );
}

describe('ProtectedRoute', () => {
  beforeEach(() => {
    mockedUseAuth.mockReset();
  });

  it('shows a loading message while the session check is in flight', () => {
    mockAuth({ isLoading: true });

    renderAt('/instructor', ['instructor']);

    expect(screen.getByText(/Loading authentication state/i)).toBeInTheDocument();
    expect(screen.queryByText('Instructor Area')).not.toBeInTheDocument();
    expect(screen.queryByText('Login Page')).not.toBeInTheDocument();
  });

  it('redirects unauthenticated users to /login', () => {
    mockAuth({ user: null, isAuthenticated: false });

    renderAt('/instructor', ['instructor']);

    expect(screen.getByText('Login Page')).toBeInTheDocument();
    expect(screen.queryByText('Instructor Area')).not.toBeInTheDocument();
  });

  it('redirects to /login when isAuthenticated is true but user is missing', () => {
    mockAuth({ user: null, isAuthenticated: true });

    renderAt('/instructor', ['instructor']);

    expect(screen.getByText('Login Page')).toBeInTheDocument();
  });

  it('redirects users with the wrong role to /404', () => {
    mockAuth({ user: makeUser('student'), isAuthenticated: true });

    renderAt('/instructor', ['instructor']);

    expect(screen.getByText('Not Found Page')).toBeInTheDocument();
    expect(screen.queryByText('Instructor Area')).not.toBeInTheDocument();
    expect(screen.queryByText('Login Page')).not.toBeInTheDocument();
  });

  it('renders children when the user has an allowed role', () => {
    mockAuth({ user: makeUser('instructor'), isAuthenticated: true });

    renderAt('/instructor', ['instructor']);

    expect(screen.getByText('Instructor Area')).toBeInTheDocument();
  });

  it('renders children for any authenticated user when no roles are specified', () => {
    mockAuth({ user: makeUser('student'), isAuthenticated: true });

    renderAt('/instructor');

    expect(screen.getByText('Instructor Area')).toBeInTheDocument();
  });
});
