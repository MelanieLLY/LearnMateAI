import { useState, useEffect } from 'react';

export interface FlashcardData {
  id: number;
  question: string;
  answer: string;
  difficulty: number;
  bloom_level: string;
}

interface FlashCard3DProps {
  card: FlashcardData;
  cardIndex: number;
  totalCards: number;
}

const BLOOM_BADGE_STYLES: Record<string, string> = {
  Remember: 'bg-blue-500/25 text-blue-100 border border-blue-400/30',
  Understand: 'bg-purple-500/25 text-purple-100 border border-purple-400/30',
  Apply: 'bg-emerald-500/25 text-emerald-100 border border-emerald-400/30',
  Analyze: 'bg-yellow-500/25 text-yellow-100 border border-yellow-400/30',
  Evaluate: 'bg-orange-500/25 text-orange-100 border border-orange-400/30',
  Create: 'bg-red-500/25 text-red-100 border border-red-400/30',
};

const DIFFICULTY_STAR_COLOR: Record<number, string> = {
  1: 'text-emerald-300',
  2: 'text-green-300',
  3: 'text-yellow-300',
  4: 'text-orange-300',
  5: 'text-red-400',
};

export default function FlashCard3D({ card, cardIndex, totalCards }: FlashCard3DProps) {
  const [isFlipped, setIsFlipped] = useState(false);

  useEffect(() => {
    setIsFlipped(false);
  }, [card.id]);

  const bloomStyle = BLOOM_BADGE_STYLES[card.bloom_level] ?? 'bg-white/20 text-white/80';
  const starColor = DIFFICULTY_STAR_COLOR[card.difficulty] ?? 'text-yellow-300';
  const stars = Array.from({ length: 5 }, (_, i) => (i < card.difficulty ? '★' : '☆')).join('');

  return (
    <div className="w-full select-none">
      {/* Progress dots */}
      <div className="flex items-center justify-between mb-5 px-1">
        <span className="text-xs font-semibold text-slate-400 uppercase tracking-widest">Flashcard</span>
        <div className="flex items-center gap-1">
          {Array.from({ length: totalCards }, (_, i) => (
            <div
              key={i}
              className="rounded-full transition-all duration-300"
              style={{
                height: '6px',
                width: i === cardIndex ? '20px' : '6px',
                background: i === cardIndex ? '#16a34a' : '#e2e8f0',
              }}
            />
          ))}
        </div>
        <span className="text-xs font-semibold text-slate-400">
          {cardIndex + 1} / {totalCards}
        </span>
      </div>

      {/* 3D Card container */}
      <div
        role="button"
        aria-label={isFlipped ? 'Flip back to question' : 'Flip to reveal answer'}
        tabIndex={0}
        onClick={() => setIsFlipped((f) => !f)}
        onKeyDown={(e) => { if (e.key === 'Enter' || e.key === ' ') setIsFlipped((f) => !f); }}
        style={{ perspective: '1200px', height: '260px' }}
        className="relative w-full cursor-pointer focus:outline-none"
      >
        {/* Inner flip container */}
        <div
          style={{
            transformStyle: 'preserve-3d',
            transition: 'transform 0.65s cubic-bezier(0.34, 1.36, 0.64, 1)',
            transform: isFlipped ? 'rotateY(180deg)' : 'rotateY(0deg)',
            position: 'relative',
            width: '100%',
            height: '100%',
          }}
        >
          {/* ——— FRONT: Question ——— */}
          <div
            style={{
              backfaceVisibility: 'hidden',
              WebkitBackfaceVisibility: 'hidden',
              position: 'absolute',
              inset: 0,
            }}
            className="rounded-2xl overflow-hidden shadow-2xl"
          >
            {/* Gradient background */}
            <div className="absolute inset-0 bg-gradient-to-br from-brand-500 via-brand-600 to-emerald-700" />
            {/* Subtle dot texture */}
            <div
              className="absolute inset-0 opacity-[0.07]"
              style={{
                backgroundImage:
                  'radial-gradient(circle, white 1px, transparent 1px)',
                backgroundSize: '24px 24px',
              }}
            />
            {/* Glowing orb */}
            <div className="absolute -top-10 -right-10 w-44 h-44 bg-white/10 rounded-full blur-3xl" />

            <div className="relative h-full flex flex-col justify-between p-7">
              {/* Badges row */}
              <div className="flex items-center justify-between">
                <span className={`text-xs font-bold px-3 py-1 rounded-full ${bloomStyle}`}>
                  {card.bloom_level}
                </span>
                <span
                  className={`text-base tracking-wider font-bold ${starColor}`}
                  title={`Difficulty: ${card.difficulty}/5`}
                >
                  {stars}
                </span>
              </div>

              {/* Question text */}
              <div className="flex-1 flex items-center justify-center py-4">
                <p className="text-white text-lg font-semibold text-center leading-relaxed drop-shadow-sm">
                  {card.question}
                </p>
              </div>

              {/* Hint */}
              <div className="flex items-center justify-center gap-1.5 opacity-60">
                <span className="text-white text-xs font-medium">Tap to reveal answer</span>
                <span className="text-white text-sm">↻</span>
              </div>
            </div>
          </div>

          {/* ——— BACK: Answer ——— */}
          <div
            style={{
              backfaceVisibility: 'hidden',
              WebkitBackfaceVisibility: 'hidden',
              transform: 'rotateY(180deg)',
              position: 'absolute',
              inset: 0,
            }}
            className="rounded-2xl overflow-hidden shadow-2xl"
          >
            {/* Dark gradient */}
            <div className="absolute inset-0 bg-gradient-to-br from-slate-700 via-slate-800 to-slate-900" />
            {/* Glowing accent */}
            <div className="absolute top-0 left-1/2 -translate-x-1/2 w-40 h-40 bg-brand-500/15 rounded-full blur-3xl" />
            <div className="absolute -bottom-10 -left-10 w-36 h-36 bg-emerald-400/10 rounded-full blur-3xl" />

            <div className="relative h-full flex flex-col justify-between p-7">
              {/* Header */}
              <div className="flex items-center justify-between">
                <span className="text-xs font-bold px-3 py-1 rounded-full bg-white/10 text-white/60">
                  Answer
                </span>
                <span className="text-xl">💡</span>
              </div>

              {/* Answer text */}
              <div className="flex-1 flex items-center justify-center py-4">
                <p className="text-white text-lg font-semibold text-center leading-relaxed">
                  {card.answer}
                </p>
              </div>

              {/* Hint */}
              <div className="flex items-center justify-center gap-1.5 opacity-60">
                <span className="text-white text-xs font-medium">Tap to flip back</span>
                <span className="text-white text-sm">↺</span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
