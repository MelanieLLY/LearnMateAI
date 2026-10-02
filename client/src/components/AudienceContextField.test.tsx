import { fireEvent, render, screen } from '@testing-library/react';
import { describe, expect, it, vi } from 'vitest';
import AudienceContextField from './AudienceContextField';
import { AUDIENCE_EXAMPLES } from './audienceExamples';

describe('AudienceContextField', () => {
  it('labels the textarea and explains where the guidelines go', () => {
    render(<AudienceContextField value="" onChange={vi.fn()} />);
    expect(screen.getByLabelText(/audience guidelines for ai/i)).toBeInTheDocument();
    expect(screen.getByText(/added to every summary, flashcard and quiz/i)).toBeInTheDocument();
  });

  it('shows one button per example', () => {
    render(<AudienceContextField value="" onChange={vi.fn()} />);
    for (const example of AUDIENCE_EXAMPLES) {
      expect(screen.getByRole('button', { name: example.label })).toBeInTheDocument();
    }
  });

  it('fills an empty field with the example text', () => {
    const onChange = vi.fn();
    render(<AudienceContextField value="" onChange={onChange} />);
    fireEvent.click(screen.getByRole('button', { name: AUDIENCE_EXAMPLES[0].label }));
    expect(onChange).toHaveBeenCalledWith(AUDIENCE_EXAMPLES[0].text);
  });

  it('appends the example on a new line after existing text', () => {
    const onChange = vi.fn();
    render(<AudienceContextField value="Grade 9 physics." onChange={onChange} />);
    fireEvent.click(screen.getByRole('button', { name: AUDIENCE_EXAMPLES[1].label }));
    expect(onChange).toHaveBeenCalledWith(`Grade 9 physics.\n${AUDIENCE_EXAMPLES[1].text}`);
  });

  it('passes typed text through', () => {
    const onChange = vi.fn();
    render(<AudienceContextField value="" onChange={onChange} />);
    fireEvent.change(screen.getByLabelText(/audience guidelines for ai/i), {
      target: { value: 'Mixed-age adult learners.' },
    });
    expect(onChange).toHaveBeenCalledWith('Mixed-age adult learners.');
  });
});
