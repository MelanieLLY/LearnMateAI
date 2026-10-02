import { useId } from 'react';
import type { JSX } from 'react';
import { AUDIENCE_EXAMPLES, MAX_AUDIENCE_CHARS } from './audienceExamples';

interface AudienceContextFieldProps {
  value: string;
  onChange: (value: string) => void;
}

export default function AudienceContextField({
  value,
  onChange,
}: AudienceContextFieldProps): JSX.Element {
  const fieldId = useId();
  const hintId = `${fieldId}-hint`;

  const addExample = (text: string): void => {
    onChange(value.trim() ? `${value.trimEnd()}\n${text}` : text);
  };

  return (
    <div className="flex flex-col gap-2">
      <label htmlFor={fieldId} className="text-sm font-semibold text-slate-700">
        Audience guidelines for AI
      </label>
      <p id={hintId} className="text-xs text-slate-500">
        Describe your students and what the AI should do or avoid. These guidelines are added to
        every summary, flashcard and quiz generated for this class.
      </p>
      <textarea
        id={fieldId}
        aria-describedby={hintId}
        maxLength={MAX_AUDIENCE_CHARS}
        placeholder="e.g. Several students are English learners; use short sentences and no idioms."
        value={value}
        onChange={(e) => onChange(e.target.value)}
        className="px-4 py-2 bg-white border border-slate-200 rounded-xl focus:outline-none focus:ring-2 focus:ring-brand-500/50 min-h-[80px]"
      />
      <div className="flex flex-wrap items-center gap-2">
        <span className="text-xs text-slate-500">Add an example:</span>
        {AUDIENCE_EXAMPLES.map((example) => (
          <button
            key={example.label}
            type="button"
            onClick={() => addExample(example.text)}
            className="px-2.5 py-1 text-xs border border-brand-200 text-brand-700 bg-brand-50 hover:bg-brand-100 rounded-lg transition-colors"
          >
            {example.label}
          </button>
        ))}
      </div>
    </div>
  );
}
