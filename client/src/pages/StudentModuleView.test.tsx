import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import { MemoryRouter } from 'react-router-dom';
import { beforeEach, describe, it, expect, vi } from 'vitest';
import StudentModuleView from './StudentModuleView';

// Mock global fetch
global.fetch = vi.fn();

const MOCK_MODULE = {
  id: 1,
  title: 'Introduction to AI',
  description: 'Basic concepts of Artificial Intelligence',
  learning_objectives: 'Understand basic AI',
  course_id: 101,
};

const MOCK_MODULE_ML = {
  id: 1,
  title: 'Advanced Machine Learning',
  description: 'Deep neural networks',
  learning_objectives: 'Learn about CNNs and RNNs',
  course_id: null,
};

const MOCK_FLASHCARDS = [
  {
    id: 1,
    question: 'What is supervised learning?',
    answer: 'Training on labelled data.',
    difficulty: 2,
    bloom_level: 'Remember',
    module_id: 1,
    student_id: 1,
    created_at: new Date().toISOString(),
  },
  {
    id: 2,
    question: 'How does backpropagation work?',
    answer: 'Computes gradients via the chain rule.',
    difficulty: 4,
    bloom_level: 'Understand',
    module_id: 1,
    student_id: 1,
    created_at: new Date().toISOString(),
  },
];

const MOCK_SUMMARY = {
  id: 1,
  title: 'AI Fundamentals Overview',
  content: 'Artificial Intelligence encompasses supervised, unsupervised, and reinforcement learning.',
  word_count: 12,
  summary_level: 'Standard',
  module_id: 1,
  student_id: 1,
  created_at: new Date().toISOString(),
};

// Helper: respond correctly to all fetch calls a component makes on mount
function mockModulesFetch(modules: object[]): void {
  (global.fetch as ReturnType<typeof vi.fn>).mockImplementation((url: string) => {
    if ((url as string) === '/api/v1/modules') {
      return Promise.resolve({ ok: true, json: async () => modules });
    }
    // Notes fetch → silently return empty so component continues
    return Promise.resolve({ ok: false, json: async () => [] });
  });
}

describe('StudentModuleView', () => {
  beforeEach(() => {
    vi.clearAllMocks();
  });

  // ——— Existing tests (must remain passing) ———

  it('renders page title and module after loading', async () => {
    (global.fetch as ReturnType<typeof vi.fn>)
      .mockResolvedValueOnce({ ok: true, json: async () => [MOCK_MODULE] })
      .mockResolvedValue({ ok: false }); // notes fetch silently fails

    render(<MemoryRouter><StudentModuleView /></MemoryRouter>);

    // Page title is always present
    expect(screen.getByText('👨🎓 学生端：模块浏览与学习')).toBeInTheDocument();

    // Module heading renders (use role to handle emoji in child <span>)
    await waitFor(() => {
      expect(screen.getByRole('heading', { name: /Introduction to AI/ })).toBeInTheDocument();
      expect(screen.getByText('Basic concepts of Artificial Intelligence')).toBeInTheDocument();
    });
  });

  it('allows user to type and submit a note', async () => {
    (global.fetch as ReturnType<typeof vi.fn>)
      .mockResolvedValueOnce({ ok: true, json: async () => [MOCK_MODULE_ML] })
      .mockResolvedValue({ ok: false });

    render(<MemoryRouter><StudentModuleView /></MemoryRouter>);

    await waitFor(() => {
      expect(screen.getByRole('heading', { name: /Advanced Machine Learning/ })).toBeInTheDocument();
    });

    // Mock the POST request for note submission
    (global.fetch as ReturnType<typeof vi.fn>).mockResolvedValueOnce({
      ok: true,
      json: async () => ({ id: 101, content: 'This is my study note', module_id: 1, student_id: 2 }),
    });

    const textarea = screen.getByPlaceholderText('在这里输入你的学习笔记、问题或心得...');
    fireEvent.change(textarea, { target: { value: 'This is my study note' } });
    expect(textarea).toHaveValue('This is my study note');

    const alertMock = vi.spyOn(window, 'alert').mockImplementation(() => {});
    fireEvent.click(screen.getByText('提交笔记'));

    await waitFor(() => {
      expect(global.fetch).toHaveBeenCalledWith(
        '/api/v1/modules/1/notes',
        expect.objectContaining({
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ content: 'This is my study note' }),
        }),
      );
    });

    await waitFor(() => {
      expect(alertMock).toHaveBeenCalledWith('Note uploaded successfully!');
      expect(textarea).toHaveValue('');
    });

    alertMock.mockRestore();
  });

  it('displays error message if fetching modules fails', async () => {
    (global.fetch as ReturnType<typeof vi.fn>).mockRejectedValueOnce(new Error('Network Error'));

    render(<MemoryRouter><StudentModuleView /></MemoryRouter>);

    await waitFor(() => {
      expect(screen.getByText(/错误: Network Error/)).toBeInTheDocument();
    });
    expect(screen.getByText('暂无可用模块')).toBeInTheDocument();
  });

  // ——— New: Tab navigation ———

  it('renders all three tabs for a loaded module', async () => {
    mockModulesFetch([MOCK_MODULE]);
    render(<MemoryRouter><StudentModuleView /></MemoryRouter>);

    await waitFor(() => {
      expect(screen.getByRole('heading', { name: /Introduction to AI/ })).toBeInTheDocument();
    });

    // All three tab buttons must be present
    expect(screen.getByRole('button', { name: /Notes/ })).toBeInTheDocument();
    expect(screen.getByRole('button', { name: /Flashcards/ })).toBeInTheDocument();
    expect(screen.getByRole('button', { name: /Summary/ })).toBeInTheDocument();
  });

  it('shows notes section by default and hides it after switching to Flashcards tab', async () => {
    mockModulesFetch([MOCK_MODULE]);
    render(<MemoryRouter><StudentModuleView /></MemoryRouter>);

    await waitFor(() => {
      expect(screen.getByRole('heading', { name: /Introduction to AI/ })).toBeInTheDocument();
    });

    // Notes tab active by default — textarea visible
    expect(screen.getByPlaceholderText('在这里输入你的学习笔记、问题或心得...')).toBeInTheDocument();

    // Switch to Flashcards tab
    fireEvent.click(screen.getByRole('button', { name: /Flashcards/ }));

    // Notes textarea must be gone
    expect(
      screen.queryByPlaceholderText('在这里输入你的学习笔记、问题或心得...'),
    ).not.toBeInTheDocument();
  });

  // ——— New: Flashcard section ———

  it('shows Generate New and Load Existing buttons in Flashcards tab', async () => {
    mockModulesFetch([MOCK_MODULE]);
    render(<MemoryRouter><StudentModuleView /></MemoryRouter>);

    await waitFor(() => {
      expect(screen.getByRole('heading', { name: /Introduction to AI/ })).toBeInTheDocument();
    });

    fireEvent.click(screen.getByRole('button', { name: /Flashcards/ }));

    expect(screen.getByText('✨ Generate New')).toBeInTheDocument();
    expect(screen.getByText('📂 Load Existing')).toBeInTheDocument();
  });

  it('calls POST flashcards endpoint and renders the card question', async () => {
    mockModulesFetch([MOCK_MODULE]);
    render(<MemoryRouter><StudentModuleView /></MemoryRouter>);

    await waitFor(() => {
      expect(screen.getByRole('heading', { name: /Introduction to AI/ })).toBeInTheDocument();
    });

    fireEvent.click(screen.getByRole('button', { name: /Flashcards/ }));

    // Mock the generate-flashcards POST
    (global.fetch as ReturnType<typeof vi.fn>).mockResolvedValueOnce({
      ok: true,
      json: async () => MOCK_FLASHCARDS,
    });

    fireEvent.click(screen.getByText('✨ Generate New'));

    await waitFor(() => {
      expect(global.fetch).toHaveBeenCalledWith(
        '/api/v1/modules/1/flashcards',
        expect.objectContaining({ method: 'POST', credentials: 'include' }),
      );
    });

    // First card question appears
    await waitFor(() => {
      expect(screen.getByText('What is supervised learning?')).toBeInTheDocument();
    });

    // Navigation controls present
    expect(screen.getByRole('button', { name: /Previous card/ })).toBeInTheDocument();
    expect(screen.getByRole('button', { name: /Next card/ })).toBeInTheDocument();
  });

  it('navigates to the second card via Next button', async () => {
    mockModulesFetch([MOCK_MODULE]);
    render(<MemoryRouter><StudentModuleView /></MemoryRouter>);

    await waitFor(() =>
      expect(screen.getByRole('heading', { name: /Introduction to AI/ })).toBeInTheDocument(),
    );

    fireEvent.click(screen.getByRole('button', { name: /Flashcards/ }));

    (global.fetch as ReturnType<typeof vi.fn>).mockResolvedValueOnce({
      ok: true,
      json: async () => MOCK_FLASHCARDS,
    });

    fireEvent.click(screen.getByText('✨ Generate New'));

    await waitFor(() => {
      expect(screen.getByText('What is supervised learning?')).toBeInTheDocument();
    });

    // Advance to card 2
    fireEvent.click(screen.getByRole('button', { name: /Next card/ }));

    await waitFor(() => {
      expect(screen.getByText('How does backpropagation work?')).toBeInTheDocument();
    });
  });

  // ——— New: Summary section ———

  it('shows level selector buttons and Generate button in Summary tab', async () => {
    mockModulesFetch([MOCK_MODULE]);
    render(<MemoryRouter><StudentModuleView /></MemoryRouter>);

    await waitFor(() =>
      expect(screen.getByRole('heading', { name: /Introduction to AI/ })).toBeInTheDocument(),
    );

    fireEvent.click(screen.getByRole('button', { name: /Summary/ }));

    // Level selector buttons have aria-pressed; use pressed option to avoid
    // matching the generate button whose text also contains "Standard"
    expect(screen.getByRole('button', { name: /Brief/, pressed: false })).toBeInTheDocument();
    expect(screen.getByRole('button', { name: /Standard/, pressed: true })).toBeInTheDocument();
    expect(screen.getByRole('button', { name: /Detailed/, pressed: false })).toBeInTheDocument();
    expect(screen.getByText('🤖 Generate Standard Summary')).toBeInTheDocument();
  });

  it('calls POST summaries with selected level and renders the summary', async () => {
    mockModulesFetch([MOCK_MODULE]);
    render(<MemoryRouter><StudentModuleView /></MemoryRouter>);

    await waitFor(() =>
      expect(screen.getByRole('heading', { name: /Introduction to AI/ })).toBeInTheDocument(),
    );

    fireEvent.click(screen.getByRole('button', { name: /Summary/ }));

    // Switch to Detailed
    fireEvent.click(screen.getByRole('button', { name: /Detailed/ }));
    expect(screen.getByText('🤖 Generate Detailed Summary')).toBeInTheDocument();

    (global.fetch as ReturnType<typeof vi.fn>).mockResolvedValueOnce({
      ok: true,
      json: async () => ({ ...MOCK_SUMMARY, summary_level: 'Detailed' }),
    });

    fireEvent.click(screen.getByText('🤖 Generate Detailed Summary'));

    await waitFor(() => {
      expect(global.fetch).toHaveBeenCalledWith(
        '/api/v1/modules/1/summaries',
        expect.objectContaining({
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ summary_level: 'Detailed' }),
        }),
      );
    });

    await waitFor(() => {
      expect(screen.getByText('AI Fundamentals Overview')).toBeInTheDocument();
      expect(
        screen.getByText(
          'Artificial Intelligence encompasses supervised, unsupervised, and reinforcement learning.',
        ),
      ).toBeInTheDocument();
    });
  });
});
