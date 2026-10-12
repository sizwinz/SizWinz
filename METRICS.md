# Automatic profile metrics

`scripts/refresh_metrics.py` fetches GitHub data, saves a public-only repository
snapshot in `assets/github-metrics.json`, and rebuilds linked project tiles and
the themed stats panel. It uses Python's standard library; no badge service is
required. Locally, authenticate with `gh`, then run:

```sh
python scripts/refresh_metrics.py
```

The `Refresh profile metrics` workflow runs hourly and can also
be run manually from Actions. Commit these changes to the repository's default
branch for the scheduled workflow to run. It uses the built-in `GITHUB_TOKEN`
with `contents: write` to commit generated assets. Repository rules must allow
the workflow's bot to push; no additional personal token is required.

- Card badges appear only for a repository with **more than 5 stars** (6 or
  above). A later refresh removes the badge if its count drops to 5 or below.
- Organization links and demo URLs have no repository star badge. EcoSpot's
  card links to its demo; set its card URL to a GitHub repository to count stars.
- Project stars combine public repositories owned by `sizwinz` and featured
  organization repositories, counting each repository once.
- Languages use code bytes across public owned repositories, excluding forks.
  The top six are listed; the gray bar remainder represents other languages.
- Commits, PRs, issues and repositories committed to use GitHub's contribution
  collection for the past year, rather than all-time totals.
- Contributions and streaks use GitHub's contribution calendar for that same
  period. The current streak allows today to be unfinished; yesterday must
  have activity. The longest streak is limited to the displayed past year.
- A failed API request aborts before replacing the last successful snapshot.
  Counts reflect the latest successful scheduled run, not each page view.

GitHub may delay scheduled runs and disables scheduled workflows in public
repositories after 60 days without activity. See [GitHub schedule documentation](https://docs.github.com/en/actions/reference/workflows-and-actions/events-that-trigger-workflows#schedule).

Offline artwork rebuild (uses the cached snapshot):

```sh
python scripts/build_composed.py
python scripts/build_cards.py
python scripts/build_stats.py
python scripts/make_readme.py
```
