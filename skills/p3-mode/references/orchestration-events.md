# Event-driven orchestration

Use this protocol for requested task queues and standing programs. A separately requested GitHub intake controller may poll for new issues. Its timer belongs to its own thread and queue, never the requested-task thread.

## Wake and hand off

- Start child work with `delegate_task` and retain its `taskId`. T3 delivers terminal results to the parent. On completion, consume the result and take the next action in the same turn.
- For pending PR checks, review, or conflicts, call `watch_pull_request` before yielding. Register each owned PR and retain the watched URL. T3's PR watcher currently polls GitHub internally; this is event-driven agent execution, not a claim of webhook-only transport.
- Before yielding with work left, dispatch every ready action. Each remaining unit must have a live child task, a registered PR watch, or an explicit blocker with its owner and resume action. A plan to act later is not a wake source. If a required event is unavailable, report that concrete gap once. Do not replace it with a heartbeat, sleep loop, or recurring timer.
- Reconcile duplicate or late events against task, owner, PR, and head before acting. Preserve paused state and accept receipts only until explicit user resume. Stop only confirmed failed writers before replacing them.
- On pause or completion, remove this run's PR watches. Retire only this run's obsolete watchdog and queued copies, identified by recorded schedule/run IDs and exact prompt. Preserve other threads' schedules and all user input. A requested issue-polling controller keeps its own intake schedule until stopped.

## Report changes, not wake-ups

The parent answers direct questions and reports decisions needing the user, a new blocker, a resolved reported blocker, a useful completed batch, and final completion. Batch related transitions into one short update. A child completion or PR event triggers work, not an automatic public status message.

Routine dispatch, review starts, passing intermediate checks, unchanged waits, and duplicate events go in the durable ledger. End a no-change automated turn without a public status reply. Required harness progress notices stay brief and substantive; do not add an extra final waiting summary.

Keep `notification-state.json` beside the queue. After sending an update, record the reported unit IDs, heads, milestone or blocker, and the next owner. Compare that record before speaking again. Repeated events with the same report key remain silent. A user asking for status always gets a current answer.

Give the operator one initial acknowledgement and one final result for an uninterrupted routine batch. Never send "checking the result", "still waiting", or a narration of the next tool call on every wake. Keep detailed receipts in the ledger and link them when useful.
