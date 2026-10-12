# Custom WakaTime card

The profile renders a compact chamfered badge with the same orange, slate and
typography as the project cards. It shows only all-time tracked hours and
minutes. Dark and light versions share the same successful snapshot.

The hourly `refresh-metrics.yml` workflow reads the public all-time badge for `sizwinz` by
default. Override the account using the repository variable `WAKATIME_USERNAME`.
To use the authenticated all-time endpoint, add the repository secret `WAKATIME_API_KEY`. The API key
is only sent in an Authorization header, never written to a file or image URL.

Only total seconds, range and refresh time are saved. Project names, files,
machines and the full private API response are excluded. Failed requests or
stats still being calculated leave the last good snapshot intact. The card
includes its successful refresh time in the SVG title; the workflow reports refresh failures.
Old weekly snapshots are never displayed as all-time totals.

GitHub schedules and image caching can delay visibility. This is an hourly
snapshot, not streaming telemetry. The first successful public fetch is saved
locally; scheduled refreshes start after the workflow is on the default branch.

```sh
WAKATIME_USERNAME=sizwinz python scripts/refresh_wakatime.py
python scripts/build_wakatime.py
```

The custom renderer uses the [official WakaTime stats API](https://wakatime.com/developers#stats).
It does not replace README.md with a third-party template; the existing README
generator continues to own profile content and links.
