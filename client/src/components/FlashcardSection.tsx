import { useState } from 'react';
import FlashCard3D, { type FlashcardData } from './FlashCard3D';

interface Flashcard extends FlashcardData {
  module_id: number;
  student_id: number;
  created_at: string;
}

interface FlashcardSectionProps {
  moduleId: number;
}

type LoadState = 'idle' | 'loading' | 'loaded';

export default function FlashcardSection({ moduleId }: FlashcardSectionProps) {
  const [flashcards, setFlashcards] = useState<Flashcard[]>([]);
  const [currentIndex, setCurrentIndex] = useState(0);
  const [loadState, setLoadState] = useState<LoadState>('idle');
  const [error, setError] = useState<string | null>(null);

  const loadFlashcards = async (method: 'GET' | 'POST') => {
    setLoadState('loading');
    setError(null);
    try {
      const res = await fetch(`/api/v1/modules/${moduleId}/flashcards`, {
        method,
        credentials: 'include',
      });
      if (!res.ok) {
        const msg = method === 'POST' ? 'Failed to generate flashcards' : 'Failed to load flashcards';
        throw new Error(msg);
      }
      const data: Flashcard[] = await res.json();
      setFlashcards(data);
      setCurrentIndex(0);
      setLoadState('loaded');
    } catch (err: unknown) {
      setError(err instanceof Error ? err.message : 'An unknown error occurred');
      setLoadState('idle');
    }
  };

  const goNext = (): void => setCurrentIndex((i) => Math.min(i + 1, flashcards.length - 1));
  const goPrev = (): void => setCurrentIndex((i) => Math.max(i - 1, 0));

  /* ——— Loading skeleton ——— */
  if (loadState === 'loading') {
    return (
      <div className="py-10 flex flex-col items-center gap-5">
        <div
          className="w-full rounded-2xl animate-pulse"
          style={{ height: '260px', background: 'linear-gradient(135deg, #e2e8f0 0%, #f1f5f9 100%)' }}
        />
        <p className="text-slate-400 text-sm font-medium animate-pulse">Generating AI flashcards…</p>
      </div>
    );
  }

  /* ——— Empty / idle prompt ——— */
  if (loadState === 'idle') {
    return (
      <div className="py-10 text-center space-y-5">
        <div className="text-5xl mb-2">🃏</div>
        <p className="text-slate-600 font-semibold">AI-Powered Flashcards</p>
        <p className="text-slate-400 text-sm max-w-xs mx-auto">
          Generate smart flashcards across all Bloom's taxonomy levels — from recall to creation.
        </p>
        {error && (
          <div className="bg-red-50 text-red-600 px-4 py-2.5 rounded-xl text-sm border border-red-100 inline-block">
            ⚠️ {error}
          </div>
        )}
        <div className="flex justify-center gap-3 pt-1">
          <button
            onClick={() => loadFlashcards('GET')}
            className="px-5 py-2.5 bg-slate-100 hover:bg-slate-200 text-slate-700 font-medium rounded-xl transition-all text-sm"
          >
            📂 Load Existing
          </button>
          <button
            onClick={() => loadFlashcards('POST')}
            className="px-5 py-2.5 bg-brand-600 hover:bg-brand-500 text-white font-semibold rounded-xl transition-all shadow-md hover:shadow-lg text-sm"
          >
            ✨ Generate New
          </button>
        </div>
      </div>
    );
  }

  /* ——— Empty result after load ——— */
  if (flashcards.length === 0) {
    return (
      <div className="py-10 text-center space-y-4">
        <div className="text-4xl">📭</div>
        <p className="text-slate-500 text-sm">No flashcards found for this module yet.</p>
        <button
          onClick={() => loadFlashcards('POST')}
          className="px-5 py-2.5 bg-brand-600 hover:bg-brand-500 text-white font-semibold rounded-xl transition-all shadow-md text-sm"
        >
          ✨ Generate Flashcards
        </button>
      </div>
    );
  }

  /* ——— Main card view ——— */
  return (
    <div className="space-y-5">
      <FlashCard3D card={flashcards[currentIndex]} cardIndex={currentIndex} totalCards={flashcards.length} />

      {/* Navigation row */}
      <div className="flex items-center gap-3">
        <button
          onClick={goPrev}
          disabled={currentIndex === 0}
          aria-label="Previous card"
          className="flex-1 py-2.5 bg-slate-100 hover:bg-slate-200 text-slate-700 font-semibold rounded-xl transition-all disabled:opacity-30 disabled:cursor-not-allowed text-sm"
        >
          ← Prev
        </button>

        <button
          onClick={() => loadFlashcards('POST')}
          aria-label="Regenerate flashcards"
          className="px-4 py-2.5 bg-white border border-slate-200 hover:border-brand-400 text-slate-500 hover:text-brand-600 font-medium rounded-xl transition-all text-xs whitespace-nowrap"
        >
          ↺ New Set
        </button>

        <button
          onClick={goNext}
          disabled={currentIndex === flashcards.length - 1}
          aria-label="Next card"
          className="flex-1 py-2.5 bg-slate-100 hover:bg-slate-200 text-slate-700 font-semibold rounded-xl transition-all disabled:opacity-30 disabled:cursor-not-allowed text-sm"
        >
          Next →
        </button>
      </div>

      {error && (
        <p className="text-red-500 text-sm text-center">⚠️ {error}</p>
      )}
    </div>
  );
}
