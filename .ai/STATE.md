# Profile README state

## Objective and status
Add live Discord presence below My setup in About; remove the setup device labels. Implemented locally; publishing and hosted verification pending.

## Verified work
- `scripts/build_profile_extras.py` retains the setup illustration with no visible device labels.
- `README.md` and `scripts/make_readme.py` embed the hosted Discord SVG with dark/light palette backgrounds, square corners, display name, and the supplied idle message.
- The service returned HTTP 200 / image/svg+xml for this Discord ID. Both themes were visually checked locally, including current Spotify activity.
- Added exactly one regression test for the absence of device labels; observed its failure before implementation, then all 10 tests passed.

## Decisions and limitations
- Use the existing hosted endpoint; no service repository edits or deployment required.
- The presence card fetches current Lanyard data on request; GitHub image caching may delay displayed changes. It is not a continuously updating stream.
- The canonical live-profile checkout is `D:/Projects/Portfolio/SizWinz`, remote `sizwinz/SizWinz`, branch `main`. The Testing checkout is the earlier design workspace.

## Next action
Commit and push the focused changes, then verify GitHub graphics validation and the rendered About section.
