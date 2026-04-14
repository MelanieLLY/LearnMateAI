import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import { MemoryRouter } from 'react-router-dom';
import { beforeEach, describe, it, expect, vi } from 'vitest';
import StudentModuleView from './StudentModuleView';

// Mock global fetch
global.fetch = vi.fn();

describe('StudentModuleView', () => {
  beforeEach(() => {
    vi.clearAllMocks();
  });

  it('renders loading state initially or fetches modules', async () => {
    // Mock 1: modules list
    (global.fetch as ReturnType<typeof vi.fn>).mockResolvedValueOnce({
      ok: true,
      json: async () => [
        {
          id: 1,
          title: 'Introduction to AI',
          description: 'Basic concepts of Artificial Intelligence',
          learning_objectives: 'Understand basic AI',
          course_id: 101,
        }
      ],
    });
    // Mock 2: notes for module 1 (component fetches these after loading modules)
    (global.fetch as ReturnType<typeof vi.fn>).mockResolvedValueOnce({
      ok: true,
      json: async () => [],
    });

    render(<MemoryRouter><StudentModuleView /></MemoryRouter>);

    // Check title renders
    expect(screen.getByText('👨‍🎓 学生端：模块浏览与学习')).toBeInTheDocument();

    // Check if the mock module was rendered
    await waitFor(() => {
      expect(screen.getByText('Introduction to AI')).toBeInTheDocument();
      expect(screen.getByText('Basic concepts of Artificial Intelligence')).toBeInTheDocument();
    });
  });

  it('allows user to type and submit a note', async () => {
    // Mock 1: modules list
    (global.fetch as ReturnType<typeof vi.fn>).mockResolvedValueOnce({
      ok: true,
      json: async () => [
        {
          id: 1,
          title: 'Advanced Machine Learning',
          description: 'Deep neural networks',
          learning_objectives: 'Learn about CNNs and RNNs',
          course_id: null,
        }
      ],
    });
    // Mock 2: notes for module 1
    (global.fetch as ReturnType<typeof vi.fn>).mockResolvedValueOnce({
      ok: true,
      json: async () => [],
    });

    render(<MemoryRouter><StudentModuleView /></MemoryRouter>);

    // Wait for modules to load
    await waitFor(() => {
      expect(screen.getByText('Advanced Machine Learning')).toBeInTheDocument();
    });

    // Mock the POST request for note submission
    (global.fetch as ReturnType<typeof vi.fn>).mockResolvedValueOnce({
      ok: true,
      json: async () => ({ id: 101, content: 'This is my study note', module_id: 1, student_id: 2 })
    });

    // Find the textarea and type a note
    const textarea = screen.getByPlaceholderText('在这里输入你的学习笔记、问题或心得...');
    fireEvent.change(textarea, { target: { value: 'This is my study note' } });

    expect(textarea).toHaveValue('This is my study note');

    // Find submit button and click
    const submitButton = screen.getByText('提交笔记');
    
    // Ensure we alert the user after success (mocking window.alert)
    const alertMock = vi.spyOn(window, 'alert').mockImplementation(() => {});

    fireEvent.click(submitButton);

    // Assert fetch was called with right POST data
    await waitFor(() => {
      expect(global.fetch).toHaveBeenCalledWith('/api/v1/modules/1/notes', expect.objectContaining({
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ content: 'This is my study note' })
      }));
    });

    // Expect alert and cleared textarea
    await waitFor(() => {
      expect(alertMock).toHaveBeenCalledWith('Note uploaded successfully!');
      expect(textarea).toHaveValue(''); // Reset state
    });

    alertMock.mockRestore();
  });

  it('displays error message if fetching modules fails', async () => {
    (global.fetch as ReturnType<typeof vi.fn>).mockRejectedValueOnce(new Error('Network Error'));

    render(<MemoryRouter><StudentModuleView /></MemoryRouter>);

    await waitFor(() => {
      expect(screen.getByText(/错误: Network Error/)).toBeInTheDocument();
      expect(screen.getByText('暂无可用模块')).toBeInTheDocument();
    });
  });
});
