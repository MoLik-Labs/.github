# MoLik Labs · Organization profile

[Profile source](profile/README.md) · [Live organization](https://github.com/MoLik-Labs)

Edit the introduction and field guide in `profile/README.md`. The Catppuccin Mocha masthead is a standalone SVG in `profile/assets/`.

The **Refresh organization profile** workflow runs daily at 03:37 UTC or manually from Actions on the default branch. It only replaces the repository index between the HTML markers and only commits changed output. Enable Actions and allow the workflow token to push to the default branch; no personal access token is needed.

To preview locally, run `python3 scripts/update.py` with an authenticated GitHub CLI, then inspect `git diff -- profile/README.md`.
