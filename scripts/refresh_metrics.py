#!/usr/bin/env python3
"""Fetch public GitHub metrics and rebuild profile artwork (stdlib only).

Use GITHUB_TOKEN in Actions, or an authenticated `gh` locally. Failed fetches
leave the last successful snapshot and artwork intact. No credentials persist.
"""
import json
import os
import subprocess
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
from urllib.request import Request, urlopen

from build_cards import CARDS, main as build_cards
from build_stats import main as build_stats

ROOT = Path(__file__).resolve().parents[1]
USER = "sizwinz"


def graphql(query, variables, token):
    request = Request("https://api.github.com/graphql",
                      data=json.dumps({"query": query, "variables": variables}).encode(),
                      headers={"Authorization": f"Bearer {token}",
                               "Content-Type": "application/json",
                               "User-Agent": "sizwinz-profile-metrics"})
    with urlopen(request, timeout=60) as response:
        result = json.load(response)
    if result.get("errors"):
        raise RuntimeError(result["errors"])
    return result["data"]


def fetch(token):
    query = """query($login:String!, $cursor:String) {
      user(login:$login) {
        repositories(first:100, after:$cursor, privacy:PUBLIC, ownerAffiliations:OWNER) {
          pageInfo { hasNextPage endCursor }
          nodes { nameWithOwner stargazerCount isFork
            languages(first:100) { edges { size node { name color } } }
          }
        }
        contributionsCollection {
          startedAt endedAt totalCommitContributions
          totalPullRequestContributions totalIssueContributions
          totalRepositoriesWithContributedCommits
          contributionCalendar { totalContributions weeks {
            contributionDays { date contributionCount }
          } }
        }
      }
    }"""
    cursor = None
    repos = {}
    languages = Counter()
    colors = {}
    while True:
        user = graphql(query, {"login": USER, "cursor": cursor}, token)["user"]
        if not user:
            raise RuntimeError("GitHub user was not found")
        connection = user["repositories"]
        for repo in connection["nodes"]:
            repos[repo["nameWithOwner"]] = repo["stargazerCount"]
            if not repo["isFork"]:
                for edge in repo["languages"]["edges"]:
                    languages[edge["node"]["name"]] += edge["size"]
                    colors[edge["node"]["name"]] = edge["node"]["color"]
        if not connection["pageInfo"]["hasNextPage"]:
            break
        cursor = connection["pageInfo"]["endCursor"]

    # Include featured projects maintained in organizations, without guessing
    # the repository behind a demo URL or linking organization-wide star totals.
    featured = set()
    for cards in CARDS.values():
        for _, _, url, *_ in cards:
            if url and url.startswith("https://github.com/"):
                parts = url.removeprefix("https://github.com/").split("/")
                if len(parts) == 2 and "?" not in url:
                    featured.add("/".join(parts))
    for repo in sorted(featured - repos.keys()):
        owner, name = repo.split("/")
        data = graphql("""query($owner:String!, $name:String!) {
          repository(owner:$owner,name:$name) { stargazerCount isPrivate }
        }""", {"owner": owner, "name": name}, token)["repository"]
        if not data or data["isPrivate"]:
            raise RuntimeError(f"Featured public repository unavailable: {repo}")
        repos[repo] = data["stargazerCount"]
    collection = user["contributionsCollection"]
    return {
        "updated_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "user": USER, "repositories": repos,
        "project_stars": sum(repos.values()),
        "languages": [{"name": name, "bytes": size, "color": colors[name]}
                      for name, size in languages.most_common()],
        "contributions": collection,
    }


def main():
    token = os.environ.get("GITHUB_TOKEN") or os.environ.get("GH_TOKEN")
    if not token:
        token = subprocess.run(["gh", "auth", "token"], check=True,
                               capture_output=True, text=True).stdout.strip()
    data = fetch(token)
    path = ROOT / "assets" / "github-metrics.json"
    temporary = path.with_suffix(".tmp")
    temporary.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")
    temporary.replace(path)
    build_cards()
    build_stats()
    qualifying = {repo: stars for repo, stars in data["repositories"].items() if stars > 5}
    print("Metrics refreshed; repositories above 5 stars:", qualifying)


if __name__ == "__main__":
    main()
