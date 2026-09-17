import json
import os
import urllib.request

BASE = "https://oddspapi-bridge.vimex-if.workers.dev"

HEADERS = {
    "User-Agent": "oddspapi-mirror/1.0",
    "Accept": "application/json",
}


def fetch_json(url):
    req = urllib.request.Request(url, headers=HEADERS)

    with urllib.request.urlopen(req, timeout=60) as response:
        return json.loads(response.read().decode("utf-8"))


def save_json(path, data):
    os.makedirs(os.path.dirname(path), exist_ok=True)

    with open(path, "w", encoding="utf-8") as f:
        json.dump(
            data,
            f,
            ensure_ascii=False,
            indent=2,
        )


def update_game(game):
    print(f"Fetching {game} matches...")

    matches = fetch_json(
        f"{BASE}/getMatches?game={game}"
    )

    save_json(
        f"data/{game}.json",
        matches,
    )

    fixture_ids = []

    for match in matches.get("matches", []):
        fixture_id = match.get("fixtureId")

        if fixture_id:
            fixture_ids.append(fixture_id)

    print(
        f"{game}: {len(fixture_ids)} fixtures with odds"
    )

    for fixture_id in fixture_ids:
        try:
            print(f"Fetching odds: {fixture_id}")

            odds = fetch_json(
                f"{BASE}/getMatchOdds?fixtureId={fixture_id}"
            )

            save_json(
                f"data/odds/{fixture_id}.json",
                odds,
            )

        except Exception as e:
            print(
                f"Failed odds for {fixture_id}: {e}"
            )


def main():
    update_game("cs2")
    update_game("dota2")

    print("Mirror update complete.")


if __name__ == "__main__":
    main()
