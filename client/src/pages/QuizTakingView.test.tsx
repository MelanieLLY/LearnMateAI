import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import { MemoryRouter, Route, Routes } from 'react-router-dom';
import { describe, it, expect, vi, beforeEach } from 'vitest';
import QuizTakingView from './QuizTakingView';

// ---------------------------------------------------------------------------
// Fixtures
// ---------------------------------------------------------------------------
const MOCK_QUIZ = {
  id: 1,
  module_id: 3,
  student_id: 2,
  title: 'Neural Networks Quiz',
  difficulty_level: 'Medium',
  questions: [
    {
      id: 1,
      text: 'What is backpropagation?',
      question_type: 'multiple_choice',
      options: [
        'A forward pass algorithm',
        'A gradient descent variant',
        'An optimisation of error by chain rule',
        'A weight initialisation method',
      ],
      correct_answer: 'An optimisation of error by chain rule',
      explanation:
        'Backpropagation computes gradients by applying the chain rule backwards through the network.',
    },
    {
      id: 2,
      text: 'Describe the vanishing gradient problem.',
      question_type: 'short_answer',
      options: null,
      correct_answer:
        'Gradients shrink exponentially as they propagate back through many layers.',
      explanation:
        'The vanishing gradient problem stops early layers from learning in deep networks.',
    },
  ],
  created_at: '2026-04-13T10:00:00Z',
};

// ---------------------------------------------------------------------------
// Helper
// ---------------------------------------------------------------------------
function renderWithRouter(moduleId = '3') {
  return render(
    <MemoryRouter initialEntries={[`/student/quiz/${moduleId}`]}>
      <Routes>
        <Route path="/student/quiz/:moduleId" element={<QuizTakingView />} />
        <Route path="/student" element={<div>Student Page</div>} />
      </Routes>
    </MemoryRouter>,
  );
}

// ---------------------------------------------------------------------------
// Tests
// ---------------------------------------------------------------------------
describe('QuizTakingView', () => {
  beforeEach(() => {
    vi.clearAllMocks();
    global.fetch = vi.fn();
  });

  it('renders difficulty selector and generate button on initial load', () => {
    renderWithRouter();

    expect(screen.getByText('Easy')).toBeInTheDocument();
    expect(screen.getByText('Medium')).toBeInTheDocument();
    expect(screen.getByText('Hard')).toBeInTheDocument();
    expect(
      screen.getByRole('button', { name: /generate quiz/i }),
    ).toBeInTheDocument();
  });

  it('calls POST /api/v1/modules/:id/quizzes when Generate Quiz is clicked', async () => {
    (global.fetch as ReturnType<typeof vi.fn>).mockResolvedValueOnce({
      ok: true,
      json: async () => MOCK_QUIZ,
    });

    renderWithRouter();
    fireEvent.click(screen.getByRole('button', { name: /generate quiz/i }));

    await waitFor(() => {
      expect(global.fetch).toHaveBeenCalledWith(
        '/api/v1/modules/3/quizzes',
        expect.objectContaining({
          method: 'POST',
          body: JSON.stringify({ difficulty_level: 'Medium' }),
        }),
      );
    });
  });

  it('shows loading spinner while the quiz is being generated', () => {
    // Never resolves — keeps the component in loading phase
    (global.fetch as ReturnType<typeof vi.fn>).mockReturnValueOnce(
      new Promise(() => {}),
    );

    renderWithRouter();
    fireEvent.click(screen.getByRole('button', { name: /generate quiz/i }));

    expect(screen.getByTestId('quiz-loading')).toBeInTheDocument();
  });

  it('displays first question and progress indicator after quiz loads', async () => {
    (global.fetch as ReturnType<typeof vi.fn>).mockResolvedValueOnce({
      ok: true,
      json: async () => MOCK_QUIZ,
    });

    renderWithRouter();
    fireEvent.click(screen.getByRole('button', { name: /generate quiz/i }));

    await waitFor(() => {
      expect(screen.getByText('What is backpropagation?')).toBeInTheDocument();
      expect(screen.getByText('Question 1 of 2')).toBeInTheDocument();
    });
  });

  it('highlights selected multiple-choice option with ring-2 class', async () => {
    (global.fetch as ReturnType<typeof vi.fn>).mockResolvedValueOnce({
      ok: true,
      json: async () => MOCK_QUIZ,
    });

    renderWithRouter();
    fireEvent.click(screen.getByRole('button', { name: /generate quiz/i }));
    await waitFor(() => screen.getByText('What is backpropagation?'));

    const optionSpan = screen.getByText('A gradient descent variant');
    fireEvent.click(optionSpan.closest('button')!);

    expect(optionSpan.closest('button')).toHaveClass('ring-2');
  });

  it('advances to next question when Next is clicked after selecting an answer', async () => {
    (global.fetch as ReturnType<typeof vi.fn>).mockResolvedValueOnce({
      ok: true,
      json: async () => MOCK_QUIZ,
    });

    renderWithRouter();
    fireEvent.click(screen.getByRole('button', { name: /generate quiz/i }));
    await waitFor(() => screen.getByText('What is backpropagation?'));

    // Select a MC option
    fireEvent.click(
      screen.getByText('An optimisation of error by chain rule').closest('button')!,
    );
    fireEvent.click(screen.getByRole('button', { name: /next/i }));

    await waitFor(() => {
      expect(
        screen.getByText('Describe the vanishing gradient problem.'),
      ).toBeInTheDocument();
      expect(screen.getByText('Question 2 of 2')).toBeInTheDocument();
    });
  });

  it('shows results screen with score badge after final submission', async () => {
    (global.fetch as ReturnType<typeof vi.fn>).mockResolvedValueOnce({
      ok: true,
      json: async () => MOCK_QUIZ,
    });

    renderWithRouter();
    fireEvent.click(screen.getByRole('button', { name: /generate quiz/i }));
    await waitFor(() => screen.getByText('What is backpropagation?'));

    // Q1: correct MC answer
    fireEvent.click(
      screen.getByText('An optimisation of error by chain rule').closest('button')!,
    );
    fireEvent.click(screen.getByRole('button', { name: /next/i }));

    // Q2: short answer
    await waitFor(() =>
      screen.getByPlaceholderText(/type your answer here/i),
    );
    fireEvent.change(screen.getByPlaceholderText(/type your answer here/i), {
      target: { value: 'Gradients shrink exponentially' },
    });
    fireEvent.click(screen.getByRole('button', { name: /submit quiz/i }));

    await waitFor(() => {
      expect(screen.getByTestId('score-badge')).toBeInTheDocument();
      expect(screen.getByText(/your score/i)).toBeInTheDocument();
    });
  });

  it('shows LLM explanation for each question in the results review', async () => {
    (global.fetch as ReturnType<typeof vi.fn>).mockResolvedValueOnce({
      ok: true,
      json: async () => MOCK_QUIZ,
    });

    renderWithRouter();
    fireEvent.click(screen.getByRole('button', { name: /generate quiz/i }));
    await waitFor(() => screen.getByText('What is backpropagation?'));

    fireEvent.click(
      screen.getByText('An optimisation of error by chain rule').closest('button')!,
    );
    fireEvent.click(screen.getByRole('button', { name: /next/i }));

    await waitFor(() => screen.getByPlaceholderText(/type your answer here/i));
    fireEvent.change(screen.getByPlaceholderText(/type your answer here/i), {
      target: { value: 'Gradients shrink' },
    });
    fireEvent.click(screen.getByRole('button', { name: /submit quiz/i }));

    await waitFor(() => {
      expect(
        screen.getByText(
          'Backpropagation computes gradients by applying the chain rule backwards through the network.',
        ),
      ).toBeInTheDocument();
      expect(
        screen.getByText(
          'The vanishing gradient problem stops early layers from learning in deep networks.',
        ),
      ).toBeInTheDocument();
    });
  });

  it('shows error message if quiz generation fails', async () => {
    (global.fetch as ReturnType<typeof vi.fn>).mockResolvedValueOnce({
      ok: false,
      status: 500,
    });

    renderWithRouter();
    fireEvent.click(screen.getByRole('button', { name: /generate quiz/i }));

    await waitFor(() => {
      expect(
        screen.getByText(/failed to generate quiz/i),
      ).toBeInTheDocument();
    });
  });

  it('sends the selected difficulty in the POST body', async () => {
    (global.fetch as ReturnType<typeof vi.fn>).mockResolvedValueOnce({
      ok: true,
      json: async () => ({ ...MOCK_QUIZ, difficulty_level: 'Hard' }),
    });

    renderWithRouter();
    fireEvent.click(screen.getByText('Hard'));
    fireEvent.click(screen.getByRole('button', { name: /generate quiz/i }));

    await waitFor(() => {
      expect(global.fetch).toHaveBeenCalledWith(
        '/api/v1/modules/3/quizzes',
        expect.objectContaining({
          body: JSON.stringify({ difficulty_level: 'Hard' }),
        }),
      );
    });
  });
});
