# p3-stack

p3-stack is [pstack](https://github.com/cursor/plugins/tree/main/pstack) rebuilt for T3 Code. Same engineering discipline, native T3 orchestration.

pstack is poteto's answer to AI slop code. It turns an agent into an engineering team: one mode skill that routes to playbooks, principles that ground every decision, and verification strict enough that you can parallelize with confidence. p3-stack keeps that system and rewires the mechanics to T3 Code's primitives:

- **Delegation.** `delegate_task` child agents replace Cursor's Task tool, with per-role providers and models resolved from `orchestrator_capabilities`. Cross-model panels are native.
- **Worktrees.** `delegate_task` with `isolation: "worktree"` gives a child its own checkout. One writer per worktree, enforced by the app instead of by advice.
- **Watching.** `watch_pull_request` wakes the thread when checks finish, someone comments, or the branch conflicts. No polling loops.
- **Scheduling.** `schedule_task` runs audits and overnight cadences even when no turn is active. No `/loop`.
- **Memory.** `t3_thread_read` and `t3_thread_search` replace mining Cursor transcript files.
- **Proof.** `preview_*` browser tools and `device_*` simulators replace external control skills. Screenshots and recordings land in the thread.

## Install

```bash
git clone https://github.com/uzairansaruzi/p3-stack.git
cd p3-stack
./install.sh
```

`install.sh` links skills into both `~/.agents/skills/` for Codex and `~/.claude/skills/` for Claude. Claude does not discover skills installed only under `.agents/`. For global Claude installs, `CLAUDE_CONFIG_DIR` overrides `~/.claude`.

Use `./install.sh --project /path/to/repo` for project-local links under both `.agents/skills/` and `.claude/skills/`. Select one provider with `--provider codex` or `--provider claude`. Existing files, directories, and links to other sources are preserved and reported as skipped. Re-running the installer leaves correct links unchanged. Keep the checkout in place because the links point into it. Skills become available in a fresh provider session. Claude documents [symlinked skill directories](https://code.claude.com/docs/en/skills#where-skills-live). Its [AGENTS.md support](https://code.claude.com/docs/en/memory#agentsmd) applies to project instructions and does not make `.agents/skills/` a Claude discovery path.

For role configuration, readers use the project root's `p3-models.md`, then `~/.agents/p3-models.md`. This is a data file and works for both providers.

Run `python3 -m unittest discover -s tests -v` to check installation and `python3 scripts/verify-skills.py` to validate skill metadata, references, and T3 portability.

## Get started

1. Run `/setup-p3`. It reads `orchestrator_capabilities` and writes `p3-models.md`, mapping each role (code, judgment, the review panels) to a provider and model you actually have.
2. Use `/p3-mode` whenever you want rigorous work. It reads the request, picks a playbook, and runs the other skills as the steps need them. Start a standing program with `/p3-mode coordinator P3_ROLE=coordinator` so the coordinator guard activates.
3. For several features, open one thread in the target repository and send the prompt below. The parent proves the first unit before parallel work and advances on child and PR events. Requested task queues need no cron thread. Keep GitHub issue polling in a separate controller thread.
4. Stuck or unsure which skill fits? Ask `/p3-help`.

```text
/p3-mode
Implement feature one, feature two, and feature three. Run this finite queue through reviewed, verified PRs and merge them. Use only the Codex Sol and Luna models for this run. Follow this repository's verification skill. Keep unrelated improvements in a backlog.
```

Expect one initial acknowledgement, batched milestone or blocker updates, and a final result. Routine transitions stay in the ledger. Each finished unit needs a real verification receipt and an independent review. A worktree isolates files, so live app work uses one designated isolated verifier. To retain merge control, replace the merge instruction with `build a reviewed stack; I will land it`.

## The mode

`p3-mode` routes every task. Its playbooks: investigation, bug fix, perf issue, hillclimb, runtime forensics, trace forensics, feature, refactoring, prototype, visual parity, authoring a skill, eval, babysit, shipping, autonomous run, orchestrate, autopilot-full, autopilot-stack, session pickup, pause safely, multi-phase plan, worktree cleanup, opening a PR.

The thread that receives `/p3-mode` runs the playbook. It owns the todo list and every `delegate_task` spawn. [`agents/p3-agent.md`](agents/p3-agent.md) wraps the delegates a run spawns. Never delegate the playbook itself to it.

## Skills

architect, arena, automate-me, benchmark-checklist, blast-radius, bro, correct, create-formal-verification-skill, create-verification-skill, figure-it-out, how, interrogate, in-your-own-words, ketchup, maintain-formal-verification-skill, maintain-verification-skill, make-bot-ui, no-comments, p3-help, recall, reflect, setup-p3, sharpen, show-me-your-work, swarm, tdd, teach, technical-writing, typescript-best-practices, unslop, why.

## Principles

The twenty-four principle skills are indexed inside `p3-mode` and referenced by the other skills by name.

## Staying current with pstack

[`UPSTREAM`](UPSTREAM) pins the pstack commit this repo matches, and [`CHANGES.md`](CHANGES.md) records every sync and every p3-only change.

```bash
scripts/upstream.sh status   # upstream commits since the pin
scripts/upstream.sh files    # changed upstream files mapped to p3-stack paths
scripts/upstream.sh diff     # the upstream diff to port
scripts/upstream.sh pin      # move the pin once the port is done
```

Port each diff through the Cursor to T3 Code map in [AGENTS.md](AGENTS.md#syncing-with-upstream-pstack), never by copying upstream files.

## Credit

p3-stack adapts [pstack](https://github.com/cursor/plugins/tree/main/pstack) by [poteto](https://x.com/poteto). The skills, principles, and language are hers; the T3 Code rewiring is this repo's. MIT, see [LICENSE](LICENSE).
