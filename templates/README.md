# Generation-time templates

`tool-page.html` embeds `text-input.html` or `structured-input.html` and the CSS/JavaScript in `fragments/`. `scripts/tool_framework.py` substitutes known `@@TOKEN@@` markers in one pass, escapes HTML metadata and safely encodes script metadata. Output pages are independent of these template files at runtime.

Use `python scripts/create_tool.py --id TOOL_ID --dry-run` before generation. Bundles are ignored, clearly unfinished and leave registry/homepage untouched. Existing files are never overwritten. Do not publish templates or mistake a working Clear/Copy interface for an implemented transformation.

See [the contract](../TOOL_CONTRACT.md) and [the guide](../TOOL_DEVELOPMENT_GUIDE.md) for the logic adapter, test-case schemas, special-purpose exceptions and manual promotion. When editing fragments, run `python scripts/verify_tool_templates.py`, Python tests and both Node test files. Existing generated/released pages are not automatically migrated.
