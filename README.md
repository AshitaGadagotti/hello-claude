# hello-claude

A tiny command-line to-do list. This was a learning project, not a real app —
built to practice Python basics.

## What it does

Add, list, complete, and delete tasks. Tasks are stored in a local
`tasks.json` file (git-ignored, so everyone starts with an empty list).

## Usage

```bash
./todo.py add "Buy milk"
./todo.py list
./todo.py done 1
./todo.py delete 1
```

## What I learned

- **argparse subcommands** — using `add_subparsers` to give each command
  (`add`, `list`, `done`, `delete`) its own arguments and help text, instead
  of hand-rolling argument parsing.
- **JSON as storage** — reading and writing a list of dicts to a file with
  `json.load`/`json.dump`, and why `indent=2` makes the file readable when
  you peek at it by hand.
- **Graceful error handling** — checking that `tasks.json` actually contains
  a valid array of well-formed tasks before trusting it, and failing with a
  clear message (and non-zero exit code) instead of a stack trace when it
  doesn't.

## Notes

No tests, no packaging, no plans to publish it. It does what it needs to do
for one person's to-do list.
