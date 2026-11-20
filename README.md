# Tekyous agent skills: tech stack diagrams for AI agents

Skills and plugins that bring [Tekyous](https://tekyous.dev?utm_source=github&utm_medium=readme), the tech stack
builder and developer tools catalogue, into your coding agent. The first one draws tech stack diagrams.

Ask your coding agent to draw your project's tech stack. It reads the repository, draws the tools it uses with their
logos, saves the picture and adds it to your README. The picture links to the same diagram in the
[Tekyous stack builder](https://tekyous.dev/builder?utm_source=github&utm_medium=readme), fully editable.

This repository packages that for agents: a **Claude Code plugin** and a **skill** for any agent with a shell. Both
use the free [Tekyous MCP server](https://tekyous.dev/mcp?utm_source=github&utm_medium=readme), which needs no
sign-in and no API key.

[![AI SaaS tech stack: tech stack diagram made with tekyous.dev](examples/ai-saas.png)](https://tekyous.dev/builder?utm_source=github&utm_medium=readme#doc=v1.VZCxTsQwDIZfJfLAQjuwdkNi4KRDQup4usEkpg3XS6LYLZyqvjsu9CC3xc73f3Yyw3vMZxRoQOh0iSPXzmOX8QwVTJTZxwDNQwXiZSClHnemRWyNkO0NC9qTgl2OY2JoDjN4pxCmBEXkt4pxWBEI9CUfvHbQD58-OMsMx6W6Zn0Z3ZVJ3cfSUKOv2enYGXgYO6XsgKMjJS0m-VkY9vsXWP6lDgUL7dNWbuI_EY8J35BvVa-RpcvE5t5MZCVmLs1MefKWuLC3Reu6-tVc4yi9XrBkn9Y5KqbgivfHVLqedbgPnbkzW__2L1YTBckXPSRF-9ip6rh8Aw)

*An AI SaaS stack drawn by the Tekyous MCP server. Click it to open the diagram in the builder and edit it.*

## Install

Pick one. Then ask: **"Draw this project's tech stack, save the image into the repo and add it to the README."**

### Claude Code: the plugin

```
/plugin marketplace add tekyous/agent-skills
/plugin install tekyous@tekyous
```

It adds the Tekyous MCP server and the `tech-stack-diagram` skill. The skill starts by itself when you ask for a
tech stack diagram, or run it as `/tekyous:tech-stack-diagram`. Grok Build installs the same plugin:
`grok plugin install tekyous/agent-skills`.

### Any agent with skills: the skill

```bash
npx skills add tekyous/agent-skills
```

Or copy [`skills/tech-stack-diagram`](skills/tech-stack-diagram) into your agent's skills folder:

| Agent | Project folder | User folder |
|---|---|---|
| Claude Code | `.claude/skills/` | `~/.claude/skills/` |
| Codex | `.agents/skills/` | `~/.agents/skills/` |
| Cursor | `.agents/skills/` or `.cursor/skills/` | `~/.cursor/skills/` |
| GitHub Copilot | `.agents/skills/` | `~/.copilot/skills/` |
| Antigravity | `.agents/skills/` | `~/.gemini/config/skills/` |
| Grok Build | `.grok/skills/` | `~/.grok/skills/` |
| Z Code | `.zcode/skills/` | `~/.zcode/skills/` |
| Cline | `.agents/skills/` | `~/.agents/skills/` |
| OpenCode | `.agents/skills/` | `~/.config/opencode/skills/` |
| Kilo Code | `.agents/skills/` | `~/.kilo/skills/` |
| Qwen Code | `.qwen/skills/` | `~/.qwen/skills/` |
| Kiro CLI | `.kiro/skills/` | `~/.kiro/skills/` |

Many agents also read the shared `.agents/skills/` folder, and `npx skills add` knows more than 75 of them.

The skill works with or without the MCP server connected (see [How it works](#how-it-works)).

### Any MCP client: the server only

Add `https://mcp.tekyous.dev/mcp` as a remote (streamable HTTP) MCP server. Setup for Claude, Cursor, VS Code with
GitHub Copilot, Codex, Antigravity, Grok Build, Z Code and other agents: [tekyous.dev/mcp](https://tekyous.dev/mcp?utm_source=github&utm_medium=readme#setup).

```bash
claude mcp add --transport http --scope user tekyous https://mcp.tekyous.dev/mcp   # Claude Code
codex mcp add tekyous --url https://mcp.tekyous.dev/mcp                             # Codex
```

## How it works

The skill reads the project's manifests and config (`package.json`, `pyproject.toml`, `requirements.txt`,
`Dockerfile`, `docker-compose.yml`, CI workflows, the README). It writes a small diagram spec: the tools, in a few
groups by role. Then it draws the spec by the first route that works:

1. **The MCP tools, when the Tekyous server is connected** (the plugin connects it). The agent looks tools up in the
   catalogue with `search_tools` and draws with `compose_diagram`.
2. **curl, when it isn't.** The same server, called over plain HTTPS: no key, no session, the same picture.
3. **An offline link, when there is no network** (Codex blocks network for shell commands by default). A local
   script encodes the spec into a `tekyous.dev/builder#doc=…` link. You open it and export the image in the builder.

Each route ends with a PNG (or, offline, the link) and a README snippet whose picture links to the editable diagram.
The server checks the spec against the Tekyous catalogue: it suggests catalogue slugs for tools drawn as custom ones
and warns about missing pieces or tools that conflict. The agent fixes what it can and draws again.

Tekyous draws a **tech stack**: the tools a project uses and, if you ask, how they connect. It does not draw code
structure, C4 levels, sequence or entity-relationship diagrams.

## What is sent, and where

- **Sent:** the diagram spec only: tool names, group titles, captions, notes and connector labels. Never file
  contents, environment values or credentials. The skill tells the agent not to open `.env` files or keys.
- **To:** `mcp.tekyous.dev` (the server) and `img.tekyous.dev` (the image). The offline route sends nothing.
- **Stored:** images for 30 days. The diagram itself lives in its link, which anyone holding it can open, so keep
  anything private out of names and notes. Calls are logged without IP addresses for 90 days.
  Details: [tekyous.dev/privacy](https://tekyous.dev/privacy#mcp-server).
- **Not done:** no API key, no account, no install hooks, no downloaded code run. The only script is
  [`doc_link.py`](skills/tech-stack-diagram/scripts/doc_link.py), the offline encoder (Python standard library).

## What's in this repository

| Path | What it is |
|---|---|
| `skills/tech-stack-diagram/` | The skill: `SKILL.md`, the spec guidance and the offline encoder |
| `.claude-plugin/` | The Claude Code plugin (`plugin.json`) and this repository as its marketplace (`marketplace.json`) |
| `.mcp.json` | The plugin's connection to the Tekyous MCP server |
| `server.json`, `glama.json` | The server's entry in the [MCP Registry](https://registry.modelcontextprotocol.io) and its Glama listing |
| `scripts/sync_design_stack.py` | Copies the server's `design_stack` prompt into the skill, so both give the same guidance |
| `tests/` | Checks the offline links match the server's own byte for byte |

The Tekyous MCP server itself, the catalogue and the renderer are not open source. This repository holds only the
packaging and the instructions, under the MIT licence.

## Development

```bash
python3 -m unittest discover tests            # offline links match the server's encoder
python3 scripts/sync_design_stack.py --check  # the skill's guidance matches the live prompt
claude plugin validate .                      # the marketplace and plugin manifests
```

After the server's `design_stack` prompt changes, run `python3 scripts/sync_design_stack.py` and commit the result.

Something broke, or an agent drew something odd? Open an issue or write to
[contact@tekyous.dev](mailto:contact@tekyous.dev).
