import { useState } from 'react';

type SummaryLevel = 'Brief' | 'Standard' | 'Detailed';

interface Summary {
  id: number;
  title: string;
  content: string;
  word_count: number;
  summary_level: SummaryLevel;
  module_id: number;
  student_id: number;
  created_at: string;
}

interface ModuleSummarySectionProps {
  moduleId: number;
}

interface LevelConfig {
  icon: string;
  label: string;
  description: string;
  activeClass: string;
  badgeClass: string;
}

const LEVEL_CONFIG: Record<SummaryLevel, LevelConfig> = {
  Brief: {
    icon: '⚡',
    label: 'Brief',
    description: '50–100 words',
    activeClass: 'bg-blue-50 border-blue-400 text-blue-700 ring-2 ring-blue-300 ring-offset-1',
    badgeClass: 'bg-blue-100 text-blue-700 border border-blue-200',
  },
  Standard: {
    icon: '📖',
    label: 'Standard',
    description: '150–250 words',
    activeClass: 'bg-purple-50 border-purple-400 text-purple-700 ring-2 ring-purple-300 ring-offset-1',
    badgeClass: 'bg-purple-100 text-purple-700 border border-purple-200',
  },
  Detailed: {
    icon: '🔬',
    label: 'Detailed',
    description: '300–500 words',
    activeClass: 'bg-amber-50 border-amber-400 text-amber-700 ring-2 ring-amber-300 ring-offset-1',
    badgeClass: 'bg-amber-100 text-amber-700 border border-amber-200',
  },
};

export default function ModuleSummarySection({ moduleId }: ModuleSummarySectionProps) {
  const [summary, setSummary] = useState<Summary | null>(null);
  const [level, setLevel] = useState<SummaryLevel>('Standard');
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [hasGenerated, setHasGenerated] = useState(false);

  const generateSummary = async (): Promise<void> => {
    setIsLoading(true);
    setError(null);
    setHasGenerated(true);
    try {
      const res = await fetch(`/api/v1/modules/${moduleId}/summaries`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        credentials: 'include',
        body: JSON.stringify({ summary_level: level }),
      });
      if (!res.ok) throw new Error('Failed to generate summary');
      const data: Summary = await res.json();
      setSummary(data);
    } catch (err: unknown) {
      setError(err instanceof Error ? err.message : 'An unknown error occurred');
    } finally {
      setIsLoading(false);
    }
  };

  const summaryLevelConfig = summary ? LEVEL_CONFIG[summary.summary_level] : null;

  return (
    <div className="space-y-5">
      {/* Level selector */}
      <div>
        <p className="text-xs font-semibold text-slate-400 uppercase tracking-widest mb-3">
          Comprehension Level
        </p>
        <div className="flex gap-2">
          {(Object.keys(LEVEL_CONFIG) as SummaryLevel[]).map((lvl) => {
            const cfg = LEVEL_CONFIG[lvl];
            const isActive = level === lvl;
            return (
              <button
                key={lvl}
                onClick={() => setLevel(lvl)}
                aria-pressed={isActive}
                className={`flex-1 py-3 px-2 rounded-xl border text-center transition-all ${
                  isActive
                    ? cfg.activeClass
                    : 'bg-white border-slate-200 text-slate-500 hover:border-slate-300 hover:bg-slate-50'
                }`}
              >
                <span className="block text-xl mb-1">{cfg.icon}</span>
                <span className="block text-xs font-bold">{cfg.label}</span>
                <span className="block text-xs opacity-60 mt-0.5">{cfg.description}</span>
              </button>
            );
          })}
        </div>
      </div>

      {/* Generate button */}
      <button
        onClick={generateSummary}
        disabled={isLoading}
        className="w-full py-3 bg-brand-600 hover:bg-brand-500 text-white font-semibold rounded-xl transition-all shadow-md hover:shadow-lg disabled:opacity-50 disabled:cursor-not-allowed flex items-center justify-center gap-2"
      >
        {isLoading ? (
          <>
            <span
              className="inline-block animate-spin"
              style={{ display: 'inline-block' }}
            >
              ⚙️
            </span>
            Generating {level} Summary…
          </>
        ) : (
          <>🤖 Generate {level} Summary</>
        )}
      </button>

      {/* Error */}
      {error && (
        <div className="bg-red-50 text-red-600 px-4 py-3 rounded-xl text-sm border border-red-100">
          ⚠️ {error}
        </div>
      )}

      {/* Loading skeleton */}
      {isLoading && (
        <div className="bg-white rounded-2xl border border-slate-100 shadow-sm p-6 space-y-3 animate-pulse">
          <div className="h-5 bg-slate-200 rounded-lg w-2/3" />
          <div className="h-4 bg-slate-100 rounded-lg w-full" />
          <div className="h-4 bg-slate-100 rounded-lg w-5/6" />
          <div className="h-4 bg-slate-100 rounded-lg w-4/6" />
          <div className="h-4 bg-slate-100 rounded-lg w-full" />
        </div>
      )}

      {/* Summary result */}
      {summary && !isLoading && (
        <div className="bg-white rounded-2xl border border-slate-100 shadow-sm overflow-hidden">
          {/* Card header */}
          <div className="px-6 py-4 bg-gradient-to-r from-slate-50 to-white border-b border-slate-100">
            <div className="flex items-start justify-between gap-3">
              <h5 className="font-bold text-slate-800 text-base leading-snug flex-1">
                {summary.title}
              </h5>
              <div className="flex items-center gap-2 shrink-0 flex-wrap justify-end">
                {summaryLevelConfig && (
                  <span
                    className={`text-xs font-bold px-2.5 py-1 rounded-full ${summaryLevelConfig.badgeClass}`}
                  >
                    {summaryLevelConfig.icon} {summary.summary_level}
                  </span>
                )}
                <span className="text-xs text-slate-400 font-medium bg-slate-100 px-2.5 py-1 rounded-full">
                  {summary.word_count} words
                </span>
              </div>
            </div>
            <p className="text-xs text-slate-400 mt-2">
              Generated {new Date(summary.created_at).toLocaleString()}
            </p>
          </div>

          {/* Card body */}
          <div className="px-6 py-5">
            <p className="text-slate-700 leading-relaxed text-sm whitespace-pre-wrap">
              {summary.content}
            </p>
          </div>

          {/* Footer: re-generate */}
          <div className="px-6 py-3 border-t border-slate-50 flex justify-end">
            <button
              onClick={generateSummary}
              className="text-xs font-medium text-slate-400 hover:text-brand-600 transition-colors"
            >
              ↺ Regenerate
            </button>
          </div>
        </div>
      )}

      {/* Placeholder when nothing generated yet */}
      {!hasGenerated && !isLoading && (
        <div className="text-center py-8 text-slate-400 text-sm">
          <div className="text-3xl mb-3">📋</div>
          <p>Select a level and click Generate to create an AI summary</p>
        </div>
      )}
    </div>
  );
}
