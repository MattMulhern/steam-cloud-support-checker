#!/usr/bin/env python3
import sys
import json
import argparse
steam_cloud_category_id = 23

def read_games_file(filename):
    with open(filename, 'r') as f:
        return json.load(f)


def gather_supported(games):
    supported = {}
    unsupported = {}
    other = {}
    for game_id, game in games.items():
        if 'categories' not in game:
            other[game_id] = game
            continue
        category_check = [x for x in game['categories'] if x['id'] == steam_cloud_category_id]
        if category_check:
            supported[game_id] = game
        else:
            unsupported[game_id] = game
    return supported, unsupported, other


def print_support(supported={}, unsupported={}, other={}, quiet=False):
    if not quiet:
        print(f"Supported: {len(supported)}:")
        for game_id, game in supported.items():
            print(f"  {game_id}: {game['name']}")

    print(f"Unsupported: {len(unsupported)}:")
    for game_id, game in unsupported.items():
        print(f"  {game_id}: {game['name']}")

    if not quiet:
        print(f"Other: {len(other)}:")
        for game_id, game in other.items():
            name = game.get('name', 'Unknown')
            print(f"  {game_id}: {name}")

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Check Steam Cloud support for games.")
    parser.add_argument("games_file", help="Path to games.json file")
    parser.add_argument("-q", "--quiet", action="store_true", help="Suppress detailed output")
    args = parser.parse_args()

    games = read_games_file(sys.argv[1])
    supported, unsupported, other = gather_supported(games)
    print_support(supported, unsupported, other, quiet=args.quiet)
