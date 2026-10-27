# Profile README state

## Objective and status
Complete: live Discord presence, setup labels removed, compact setup padding, and four independently collapsible profile sections. Published to main.

## Verified work
- `scripts/build_profile_extras.py` retains the setup illustration with no visible device labels.
- `README.md` and `scripts/make_readme.py` embed the hosted Discord SVG using layout=readme at 744px, dark/light themes, display name, and the supplied idle message. Native renderer has a chamfered frame, activity grid, decorations, and artwork fallbacks.
- The service returned HTTP 200 / image/svg+xml for this Discord ID. Both themes were visually checked locally, including current Spotify activity.
- Three focused regressions cover absent setup labels, compact bottom padding, and independent disclosure sections. Each was observed failing before its respective change. All 12 tests pass.
- Setup panel reduced from 304px to 272px height; artwork dimensions retained and bottom padding reduced from 46px to 14px.
- Bio, setup/current activity, tech stack, and quotes now expand independently; existing biography preserved.
- GitHub rendering checked for the live Discord activity and all four disclosure rows. Graphics validation passed on implementation commit `977f212` (run `40472081738`).

## Decisions and limitations
- Use the existing hosted endpoint; no service repository edits or deployment required.
- The presence card fetches current Lanyard data on request; GitHub image caching may delay displayed changes. It is not a continuously updating stream.
- The canonical live-profile checkout is `D:/Projects/Portfolio/SizWinz`, remote `sizwinz/SizWinz`, branch `main`. The Testing checkout is the earlier design workspace.

## Next action
No remaining implementation tasks. For profile copy edits, update both README.md and scripts/make_readme.py; run python scripts/make_readme.py and the existing regeneration check.

## Native Discord renderer update
- Service source: D:/Projects/Contributions/lanyard-profile-readme; GitHub sizwinz/lanyard-profile-readme. Native layout deployed and dark/light production endpoints checked.
- Activity artwork uses Discord media proxy to preserve encoded external paths; real Arrival poster and Minecraft artwork verified locally.
- Profile tests: all 12 pass before publishing the new URL. Hosted graphics validation and final profile check pending.
