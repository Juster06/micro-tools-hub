# Local To-Do List

At most 100 tasks, each a single line of 1–200 UTF-16 units; leading/trailing whitespace is trimmed. Edit fields must be saved individually. Export/import uses versioned JSON (up to 64 KiB) and import replaces the current list only after full validation. Persistence is off by default; opt in explicitly. Enabling with a saved list restores it only if the current list is empty; otherwise disable/clear or export first. Turning off persistence removes the saved list. Storage denial or quota errors are shown and in-memory tasks remain. Locally saved tasks may be accessible to others using the same browser profile.

Input stays local; hosting and the existing styling CDN are separate requests. Publication is pending.
