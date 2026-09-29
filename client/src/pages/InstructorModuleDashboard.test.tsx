import { fireEvent, render, screen, waitFor, within } from '@testing-library/react';
import { MemoryRouter } from 'react-router-dom';
import { afterEach, beforeEach, describe, expect, it, vi } from 'vitest';
import InstructorModuleDashboard from './InstructorModuleDashboard';

const MOCK_COURSE = {
  id: 10,
  title: 'Intro to AI',
  description: 'Foundations of AI',
  audience_context: 'Undergrad',
};

const MOCK_MODULE = {
  id: 1,
  title: 'Neural Networks 101',
  description: 'Perceptrons and backprop',
  learning_objectives: null,
  audience_context: null,
  course_id: null,
  created_at: '2026-01-01T00:00:00Z',
};

const EMPTY_REPORT = {
  overall_average: 0,
  total_students: 0,
  common_gaps: [],
  module_stats: [],
};

interface MockApi {
  modules?: unknown[];
  courses?: unknown[];
  modulesOk?: boolean;
  students?: unknown[];
  report?: unknown;
}

const fetchMock = vi.fn();

function jsonResponse(body: unknown, ok = true): Response {
  return { ok, status: ok ? 200 : 500, json: async () => body } as Response;
}

function mockApi({
  modules = [],
  courses = [],
  modulesOk = true,
  students = [],
  report = EMPTY_REPORT,
}: MockApi = {}): void {
  fetchMock.mockImplementation((url: string) => {
    if (url === '/api/v1/modules') return Promise.resolve(jsonResponse(modules, modulesOk));
    if (url === '/api/v1/courses') return Promise.resolve(jsonResponse(courses));
    if (url.endsWith('/students')) return Promise.resolve(jsonResponse(students));
    if (url.endsWith('/report')) return Promise.resolve(jsonResponse(report));
    // materials, quizzes, etc.
    return Promise.resolve(jsonResponse([]));
  });
}

function renderDashboard(): void {
  render(
    <MemoryRouter>
      <InstructorModuleDashboard />
    </MemoryRouter>,
  );
}

async function waitForDashboardLoaded(): Promise<void> {
  await waitFor(() =>
    expect(screen.queryByRole('status', { name: /Loading dashboard/i })).not.toBeInTheDocument(),
  );
}

describe('InstructorModuleDashboard', () => {
  beforeEach(() => {
    fetchMock.mockReset();
    vi.stubGlobal('fetch', fetchMock);
  });

  afterEach(() => {
    vi.unstubAllGlobals();
  });

  describe('loading state', () => {
    it('shows a skeleton while modules and courses are loading', () => {
      fetchMock.mockReturnValue(new Promise<Response>(() => {}));

      renderDashboard();

      expect(screen.getByRole('status', { name: /Loading dashboard/i })).toBeInTheDocument();
      expect(screen.getByRole('heading', { name: /Instructor Dashboard/i })).toBeInTheDocument();
      expect(screen.queryByText(/Class Switcher/i)).not.toBeInTheDocument();
      expect(screen.queryByText(/No modules in current view/i)).not.toBeInTheDocument();
    });

    it('requests modules and courses with cookies on mount', () => {
      fetchMock.mockReturnValue(new Promise<Response>(() => {}));

      renderDashboard();

      expect(fetchMock).toHaveBeenCalledWith('/api/v1/modules', { credentials: 'include' });
      expect(fetchMock).toHaveBeenCalledWith('/api/v1/courses', { credentials: 'include' });
    });

    it('replaces the skeleton with the dashboard once data arrives', async () => {
      mockApi({ modules: [MOCK_MODULE], courses: [MOCK_COURSE] });

      renderDashboard();

      expect(await screen.findByText('Neural Networks 101')).toBeInTheDocument();
      expect(screen.queryByRole('status', { name: /Loading dashboard/i })).not.toBeInTheDocument();
      expect(screen.getByRole('button', { name: /Intro to AI/ })).toBeInTheDocument();
    });
  });

  describe('empty state', () => {
    it('shows an empty module list when the instructor has no modules or courses', async () => {
      mockApi({ modules: [], courses: [] });

      renderDashboard();
      await waitForDashboardLoaded();

      expect(screen.getByText(/No modules in current view/i)).toBeInTheDocument();
      expect(screen.getByText(/Class Switcher/i)).toBeInTheDocument();
      expect(screen.queryByText(/Error:/)).not.toBeInTheDocument();
    });

    it('shows empty states for a newly created class with no students, modules or data', async () => {
      mockApi({ modules: [MOCK_MODULE], courses: [MOCK_COURSE] });
      renderDashboard();
      await waitForDashboardLoaded();

      fireEvent.click(screen.getByRole('button', { name: /Intro to AI/ }));

      expect(await screen.findByText(/No students enrolled yet/i)).toBeInTheDocument();
      // The orphan module does not belong to this class, so the list is empty.
      expect(screen.getByText(/No modules in current view/i)).toBeInTheDocument();
      expect(screen.queryByText('Neural Networks 101')).not.toBeInTheDocument();

      const report = (await screen.findByText(/Class Performance Report/i)).closest('section');
      expect(report).not.toBeNull();
      const reportScope = within(report as HTMLElement);
      expect(reportScope.getByText(/Insufficient data to analyze common gaps/i)).toBeInTheDocument();
      expect(reportScope.getByText(/No module progress data available/i)).toBeInTheDocument();
    });

    it('shows a "no materials" placeholder for a module without uploads', async () => {
      mockApi({ modules: [MOCK_MODULE], courses: [] });

      renderDashboard();

      expect(await screen.findByText(/No materials uploaded yet/i)).toBeInTheDocument();
    });
  });

  describe('error state', () => {
    it('shows an error banner and stops loading when the modules request fails', async () => {
      mockApi({ modulesOk: false });

      renderDashboard();

      expect(await screen.findByText(/Error: Failed to fetch data/i)).toBeInTheDocument();
      expect(screen.queryByRole('status', { name: /Loading dashboard/i })).not.toBeInTheDocument();
    });

    it('shows the network error message when fetch rejects', async () => {
      fetchMock.mockRejectedValue(new Error('Network down'));

      renderDashboard();

      expect(await screen.findByText(/Error: Network down/i)).toBeInTheDocument();
    });
  });
});
