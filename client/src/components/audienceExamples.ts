export interface AudienceExample {
  label: string;
  text: string;
}

/**
 * Starting points for instructors writing audience guidelines. The backend appends whatever
 * the instructor saves to each agent's system prompt (server/src/agents/prompts/audience.py).
 */
export const AUDIENCE_EXAMPLES: readonly AudienceExample[] = [
  {
    label: 'Students who lost a parent',
    text:
      'Some students have lost a parent or live in foster care. Avoid examples that assume a ' +
      'student lives with or can ask their parents.',
  },
  {
    label: "Girls' school",
    text:
      "This is a girls' school. Where it fits the topic, use women scientists, engineers and " +
      'leaders as positive examples.',
  },
  {
    label: 'Check for racial bias',
    text:
      'Many students in this class are Black. Check every example and scenario for racial ' +
      'stereotypes, and include Black scientists, historical figures and professionals as ' +
      'positive examples where they fit.',
  },
];

/** Same limit as `audience_context` in server/src/schemas/course.py. */
export const MAX_AUDIENCE_CHARS = 1000;
