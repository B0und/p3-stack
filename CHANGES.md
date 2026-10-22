# Changes

Every pstack sync and every p3-only change, newest first. `UPSTREAM` holds the pstack commit the latest sync reached. See [AGENTS.md](AGENTS.md#syncing-with-upstream-pstack) for the sync steps.

## Unreleased

Finite queues use Autopilot-full with one parent-bound two-minute watchdog, completion-event reconciliation, durable task ownership, a pilot before parallel work, and two implementation owners by default. Routine work uses one designated isolated app verifier and one independent reviewer. Recovery confirms the old owner is stopped. Current user model restrictions override role defaults for the run. Orchestrate shares this contract for evolving programs. The router points to KaraRen's repository-owned Pi guards and distinguishes their enforcement from Codex execution.

Delegated worker briefs carry a `DONE WHEN` completion condition and a `BLOCKED` line instead of a `TIMEBOX` runtime cap. A unit ends when its VERIFY commands pass or its worker reports a blocker, never on a clock.

The Orchestrate Frame step sizes a program by units, expected stacks and what one agent could carry alone, and lands verified units as they arrive instead of reserving a share of a wall-clock budget. The p3-help away-mode prompt and recipe give a blocked exit instead of one measured in hours.

A user-level `p3-coordinator-guard` pi extension enforces the coordinator tool policy. It activates only when the first user message starts with `P3_ROLE=coordinator` or `/p3-mode coordinator`, allows delegation and orchestration tools plus the `orchestrate/**` store, and blocks work commands plus non-policy delegate, launch, configure, `create_threads`, fork, and project-default targets. A fork is allowed only from the current worker thread when `threadId` is omitted, because another thread's model cannot be read synchronously. A project default is allowed only when it is absent or names the worker model. `P3_COORDINATOR_GUARD=0` disables it. The p3-mode skill and Orchestrate playbook document the allowlist and the startup marker.

KaraRen owns the `kararen-no-wait-guard` Pi extension, installed with `bun run guard:install` and checked by doctor. Use T3 completion events and `task_status` rather than shell wait wrappers.

A worker twice removed the owner's `/tmp/.X11-unix/X0` with a display probe, then symlinked `X0` to `X0_` instead of reporting it. A user-level `kararen-display-guard` pi extension blocks `xvfb-run` without an explicit server number of 90 or above, `xvfb-run -a`, `-d` and `--auto-servernum`, `Xvfb` displays below 90, `-displayfd` and a no-display `Xvfb`, plus deletes, moves, links, truncations and write redirects of `/tmp/.X*-lock` and `/tmp/.X11-unix`. It allows reads and unrelated paths, activates only in `/home/unbound/Projects/KaraRen` and `/home/unbound/.t3/worktrees/KaraRen/`, and `KARAREN_DISPLAY_GUARD=0` disables it.

Issue #2 is fixed locally. The installer defaults to both provider paths, supports provider selection and `CLAUDE_CONFIG_DIR`, and preserves existing user-owned skills and foreign links. Skill creation and discovery use the active provider directory. Model readers check project configuration before the global fallback. Installer tests cover both providers and repeated installs.

T3 child worktrees now use `delegate_task` with `isolation: "worktree"`. Separate top-level threads require an explicit user request. The skill verifier checks metadata, links, configuration fallback, and unported Cursor mechanisms.

## 2026-10-21: sync pstack 0.15.25 to 0.15.29

Upstream range `09d06eb..111cf6a` (cursor/plugins, `pstack/`), pinned to the current cursor/plugins main commit.

### Ported

- **New skills `create-formal-verification-skill` and `maintain-formal-verification-skill`** (4382e68, 7b353f7, 6b78e9f). Create verifies one property where a bug costs the most and tests reach the least, with TLA+ as the default for an ordering question and a generated-inputs fallback when no verifier runs on the language. Maintain diffs covered code since the recorded sync commit, updates the model or properties from the code, reruns, and judges each failure as drift or a bug. Both are tool-neutral, so they port unchanged.
- **`setup-p3` step 8** (f9be7aa): offer once to generate a formal verification skill, as step 7 already does for a verification skill. **`p3-help`** gains the matching discovery check and two rows, plus the offer in its setup steps.
- **`sharpen` returns to the original prompt rewrite** (75fabac, 88d4751). It names what a top professional would add, their raw material, their methods, and an outside check, then hands back the rewritten prompt instead of doing the task. `p3-help` and `recipes.md` carry the new wording.
- **`ketchup` lists every waiting item and never cuts to fit a word count** (16541c6, bc14437). One call can cover many items, each item carries its link, user impact, evidence, risk, and pick, and the reply grows with the item count. The happened summary drops under 100 words. Visual guidance moves to one place and rules out drawing action items. T3 state reads stay: `list_thread_pull_requests`, `task_status`, `t3_thread_read`, `html_preview` plus `html_render`.
- **`typescript-best-practices`** (0317eb8): a brand comes from a verifying type guard, never from `as`, in both the rule table and `references/patterns.md`.

### Skipped

- **Claude Code adapter** (#705). p3 replaces harness adapters and role rules with live provider discovery through `orchestrator_capabilities` plus `p3-models.md`, so there is no `~/.claude/rules` file to write and no Cursor-only feature table to translate. The installer already handles both provider directories.
- **Guide refresh and its docs-vs-tree check** (019a6a2). p3 ships no `docs/guide`; `scripts/verify-skills.py` already checks the tree that p3 does ship.
- **`make-bot-ui` and `poteto-mode` name fixes** (a968159). p3 names every skill after its folder already; the `poteto-mode` fix has no p3 equivalent.
- Cursor plugin manifests, marketplace assets, and version bumps.

## 2026-10-17: sync pstack 0.15.20 to 0.15.25

Built on [PR #8](https://github.com/uzairansaruzi/p3-stack/pull/8), preserving its earlier 0.15.10 to 0.15.20 port. Upstream range `1b6d44f..09d06eb`, pinned to the current cursor/plugins main commit.

### Ported

- Add `in-your-own-words` and `sharpen`. Update `ketchup` to explain changes with existing screenshots, videos, and diagrams, with replies under 150 words. Autopilot ticks use it when something changes.
- Carry the revised attack-the-premise, root-cause, idempotence, caller-migration, behaviour-test, and type-system principles, plus the shorter review and shipping guidance.
- Match delegate effort to the job using detected provider options. Preserve role diversity and configured verification speed.
- Carry the autopilot merge-safety, single-verifier rules for minor revisions, and reduced orchestration guidance. Preserve T3 scheduling, PR registration, watch wake-ups, task cancellation, and isolated child worktrees.
- Resolve bundled leaf skills and worker briefs from the installation checkout. Remove ignored frontmatter and document fresh-session discovery.
- Adapt the intent of upstream Claude support through the dual-provider installer and provider-aware authoring paths. p3 remains a T3 package on both providers.

### Not copied

Cursor plugin manifests, marketplace assets, the Cursor guide, its generated Claude marketplace tree, and Cursor orchestration/watcher scripts are not shipped. T3 owns delegation and PR watching. The latest orchestration and worktree-audit script changes reinforce lifecycle and ownership rules already represented by p3 playbooks. Model-family slug substitutions are replaced by live provider discovery. The upstream README's Cursor menu and plugin commands are replaced by provider skill-directory instructions.

## 2026-10-12: sync pstack 0.15.10 → 0.15.20

Upstream range `4e5b1cf..1b6d44f` (cursor/plugins, `pstack/`).

### p3-only

- Add `UPSTREAM` (the pin) and `scripts/upstream.sh` (`status`, `files`, `diff`, `pin`) for tracking pstack.
- Add this file, the "Syncing with upstream pstack" section of `AGENTS.md`, and the "Staying current with pstack" section of the README.
- README: list `ketchup` and state that the thread receiving `/p3-mode` runs the playbook. Keep the canonical `uzairansaruzi/p3-stack` clone URL.

### Ported

- **New skill `ketchup`** (978ca6e, ea32d95). Catches the user up on everything since their last message, with an executive summary per action item. Before/after visuals use `preview_*`/`device_screenshot` captures and `html_preview` + `html_render` collages. State is read with `list_thread_pull_requests`, `task_status`, and `t3_thread_read`.
- **`p3-help`** (00b52d9, 807c031, 1e56b29). Typed-only (`disable-model-invocation: true`). New `references/prompting.md` and `references/recipes.md`, with `/loop` rewritten as "run until done". Asks once per thread about `/setup-p3` when `p3-models.md` is missing. Adds a `/ketchup` row and a `/ketchup` vs `/recall` close call.
- **The thread runs `/p3-mode`, and `p3-agent` is only a delegate** (2bd5dd4). Applied in `p3-mode/SKILL.md` and `agents/p3-agent.md`.
- **`worktree-cleanup`** (cf9a111, 08bd59b). Judge merge state against the default branch (`origin/HEAD`, then `origin/main`, then `origin/master`) or the PR target, after fetching it. Upstream fixed this in `worktree-audit.sh`; p3 carries it as prose. Intro cut.
- **`create-verification-skill`** (c49b37a). Ready means usable from an empty data dir, not a port answering. An unsatisfiable journey reports failure with the reason in Gotchas. Setup done only by a stand-in stays unverified until the real target is run.
- **`unslop`** (bc697d0). "Must always apply." is dropped from the description.
- **`setup-p3`** (df58112). The budget-to-effort map is now unlimited/large/medium/small → max/xhigh/high/medium, and the default budget is `large (xhigh)`.
- **Token-cutting distillation** (00b14f1, 08bd59b), carried through with T3 wiring kept:
  - `p3-mode`: principle leaf names and playbook paths derived from titles.
  - `babysit`, `opening-a-pr`, `trace-forensics`.
  - `architect` (+ runner prompt), `arena`, `benchmark-checklist`, `blast-radius`, `figure-it-out`, `technical-writing`.
  - `how` (+ explorer prompt), `interrogate` (+ reviewer prompt, rubric), `reflect` (+ all four reviewer/synthesizer prompts).
  - `why` (+ epistemics, investigator and synthesizer prompts, and the code-archaeology, datadog, incident-postmortem, sentry and slack sources).
  - Thirteen principles: build-the-lever, encode-lessons-in-structure, exhaust-the-design-space, explain-the-number, guard-the-context-window, laziness-protocol, minimize-reader-load, model-the-domain, never-block-on-the-human, redesign-from-first-principles, subtract-before-you-add, test-behavior-not-implementation, type-system-discipline.

### Skipped

- **Model defaults** (df58112: drop Sol, Opus `xhigh`, Grok). p3 resolves roles through `setup-p3`, so there are no slugs to swap. Upstream also shrank `interrogate` from three reviewers to two. p3 still sizes panels at one entry per detected provider, up to three. Edit the `interrogate reviewers` line in `p3-models.md` to change it.
- **Comment Sicko id rename** (de2dba6). p3 passes `agents/comment-sicko.md` as `delegate_task` brief text and has no agent id.
- **Script-only fixes** (ff8f83d watch-pr pagination, 87c8103 check-plan fenced blocks). p3 replaces `watch-pr` with `watch_pull_request` and does not ship `check-plan.mjs`.
- **Cursor packaging** (e5a02f8 Agent Plugins manifest, 1b6d44f version bump), plus the `docs/guide` refresh (2cbf585). p3 ships no Cursor manifests and no guide.
- `reflect` step 1's transcript-JSONL discovery. p3 reads threads with `t3_thread_read` and `t3_thread_search`.

## 2026-10-05: initial port of pstack 0.15.10

Ported from upstream `4e5b1cf` (pstack 0.15.10) by Uzair Ansar in `uzairansaruzi/p3-stack` (`c4824d3`, `09909eb`). It renames `poteto-mode`, `poteto-agent`, `poteto-help` and `setup-pstack` to `p3-mode`, `p3-agent`, `p3-help` and `setup-p3`, and rewires every Cursor mechanism to T3 Code per the map in `AGENTS.md`.
