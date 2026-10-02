// Tests for ai-pr-review.mjs. Run with: node --test .github/scripts/ai-pr-review.test.mjs
import assert from "node:assert/strict";
import { test } from "node:test";

import {
  COMMENT_MARKER,
  DEFAULT_MODEL,
  MAX_DIFF_CHARS,
  REVIEW_SCHEMA,
  isBlocking,
  parseReview,
  renderComment,
  runReview,
  truncateDiff,
  upsertComment,
} from "./ai-pr-review.mjs";

const PASS_REVIEW = {
  verdict: "pass",
  summary: "Small, tested change.",
  findings: [
    {
      severity: "low",
      category: "quality",
      location: "server/src/main.py:10",
      title: "Name could be clearer",
      detail: "Consider renaming x.",
    },
  ],
};

const BLOCK_REVIEW = {
  verdict: "block",
  summary: "Leaks a secret.",
  findings: [
    {
      severity: "critical",
      category: "security",
      location: "server/src/config.py:3",
      title: "Hardcoded API key",
      detail: "Move it to .env.",
    },
  ],
};

function fakeClient(review, overrides = {}) {
  const calls = [];
  return {
    calls,
    beta: {
      messages: {
        create: async (params) => {
          calls.push(params);
          return {
            stop_reason: "end_turn",
            content: [{ type: "text", text: JSON.stringify(review) }],
            ...overrides,
          };
        },
      },
    },
  };
}

function fakeGitHub(existingComments = []) {
  const requests = [];
  const fetchImpl = async (url, init) => {
    requests.push({ url, method: init.method, body: init.body ? JSON.parse(init.body) : null });
    const payload = init.method === "GET" ? existingComments : { id: 99 };
    return { ok: true, status: 200, json: async () => payload };
  };
  return { requests, fetchImpl };
}

const ENV = {
  ANTHROPIC_API_KEY: "test-key",
  GITHUB_TOKEN: "gh-test-token",
  GITHUB_REPOSITORY: "owner/repo",
  PR_NUMBER: "7",
};
const readFile = (p) => (p === "pr.diff" ? "diff --git a/x b/x\n+print('hi')\n" : "x\n");

test("schema requires a verdict enum and disallows extra keys", () => {
  assert.deepEqual(REVIEW_SCHEMA.properties.verdict.enum, ["pass", "block"]);
  assert.equal(REVIEW_SCHEMA.additionalProperties, false);
  assert.equal(REVIEW_SCHEMA.properties.findings.items.additionalProperties, false);
});

test("parseReview rejects non-JSON and bad verdicts", () => {
  assert.throws(() => parseReview("not json"), /not valid JSON/);
  assert.throws(() => parseReview('{"verdict":"maybe","summary":"","findings":[]}'), /verdict/);
  assert.equal(parseReview(JSON.stringify(PASS_REVIEW)).verdict, "pass");
});

test("isBlocking is true for a block verdict or any critical finding", () => {
  assert.equal(isBlocking(PASS_REVIEW), false);
  assert.equal(isBlocking(BLOCK_REVIEW), true);
  assert.equal(isBlocking({ ...BLOCK_REVIEW, verdict: "pass" }), true);
});

test("truncateDiff caps very large diffs", () => {
  const { diff, truncated } = truncateDiff("a".repeat(MAX_DIFF_CHARS + 5));
  assert.equal(diff.length, MAX_DIFF_CHARS);
  assert.equal(truncated, true);
});

test("renderComment carries the marker and the blocking status", () => {
  const body = renderComment(BLOCK_REVIEW, { model: "m", truncated: false });
  assert.ok(body.startsWith(COMMENT_MARKER));
  assert.match(body, /Blocking issues found/);
  assert.match(body, /CRITICAL/);
});

test("upsertComment updates the existing bot comment instead of posting a new one", async () => {
  const { requests, fetchImpl } = fakeGitHub([
    { id: 1, user: { type: "User" }, body: `${COMMENT_MARKER} quoted by a human` },
    { id: 2, user: { type: "Bot" }, body: `${COMMENT_MARKER}\nold review` },
  ]);
  const result = await upsertComment({ fetchImpl, token: "t", repo: "o/r", prNumber: 7, body: "new" });
  assert.deepEqual(result, { action: "updated", id: 2 });
  assert.equal(requests.at(-1).method, "PATCH");
  assert.match(requests.at(-1).url, /issues\/comments\/2$/);
});

test("upsertComment creates a comment when none exists", async () => {
  const { requests, fetchImpl } = fakeGitHub([]);
  const result = await upsertComment({ fetchImpl, token: "t", repo: "o/r", prNumber: 7, body: "new" });
  assert.equal(result.action, "created");
  assert.equal(requests.at(-1).method, "POST");
});

test("runReview skips without an API key and makes no requests", async () => {
  const { requests, fetchImpl } = fakeGitHub();
  const logs = [];
  const code = await runReview({
    env: { ...ENV, ANTHROPIC_API_KEY: "" },
    client: null,
    fetchImpl,
    readFile,
    log: (m) => logs.push(m),
  });
  assert.equal(code, 0);
  assert.equal(requests.length, 0);
  assert.match(logs[0], /Skipping/);
});

test("runReview passes and comments for a non-blocking review", async () => {
  const client = fakeClient(PASS_REVIEW);
  const { requests, fetchImpl } = fakeGitHub();
  const code = await runReview({ env: ENV, client, fetchImpl, readFile, log: () => {} });
  assert.equal(code, 0);
  const params = client.calls[0];
  assert.equal(params.model, DEFAULT_MODEL);
  assert.equal(params.output_config.format.type, "json_schema");
  assert.equal(params.tool_choice, undefined);
  assert.equal(requests.at(-1).method, "POST");
  assert.match(requests.at(-1).body.body, /No blocking issues/);
});

test("runReview fails the check for a blocking review", async () => {
  const { fetchImpl } = fakeGitHub();
  const code = await runReview({
    env: { ...ENV, AI_REVIEW_MODEL: "claude-sonnet-5-5" },
    client: fakeClient(BLOCK_REVIEW),
    fetchImpl,
    readFile,
    log: () => {},
  });
  assert.equal(code, 1);
});

test("runReview fails and posts an error comment on refusal", async () => {
  const { requests, fetchImpl } = fakeGitHub();
  const code = await runReview({
    env: ENV,
    client: fakeClient(PASS_REVIEW, { stop_reason: "refusal", content: [] }),
    fetchImpl,
    readFile,
    log: () => {},
  });
  assert.equal(code, 1);
  assert.match(requests.at(-1).body.body, /did not complete/);
});
