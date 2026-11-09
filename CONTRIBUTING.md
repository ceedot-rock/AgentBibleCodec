# Contributing to AgentBibleCodec

## Flow

1. Open an issue or pick an existing one.
2. Branch from the default branch (`main`): `fix/short-name`.
3. Keep diffs small and focused; one concern per pull request.
4. Open a pull request against `main` using the template. CI must pass.
5. A maintainer merges. Never push directly to `main`.

## Checks

There is no automated test suite. Keep `bible.jsonl` one record per line and keep `bible-index.json` in sync with `bible.md`; spot-check with `python -m json.tool` on touched files.

## Secrets

Never commit API keys, tokens, or credentials. If you leak one, rotate it
immediately and say so in the pull request.

## License

By contributing you agree your work is distributed under the repo's LICENSE.
