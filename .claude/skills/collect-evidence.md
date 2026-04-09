# Claude Code Skill: /collect-evidence

## Metadata
**Name:** `/collect-evidence`  
**Purpose:** Automatically log and collect markdown/Git logs as evidence for Project 3 "Claude Code Mastery" grading.  
**Version:** 1.0  

## Overview
This skill is used at the end of a sprint or feature development to automatically generate a `hw_evidence_log.md` file containing recent Git commits, testing screenshots/logs, and feature implementation footprints.

## Workflow

1. Execute a Git log command to capture the latest 5 commits.
2. Read the testing files modified recently to ensure TDD trace is visible.
3. Consolidate these findings into a `.md` artifact or log it in the terminal so the user can easily screenshot it for submission.

## Execution Prompt
When the user types `/collect-evidence`, say:
"Generating evidence log for Project 3... I will now summarize our C.L.E.A.R. reviews and recent feature branches into a dummy report."
