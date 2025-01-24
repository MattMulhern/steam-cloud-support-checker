#!/usr/bin/env python3
import requests
import json
import datetime
import time
import logging
import sys
import os

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__file__)
file_handler = logging.FileHandler(f"{__file__}.log")
file_handler.setLevel(logging.INFO)


def do_get(url, params, max_appempts=5, wait_start=60, wait_increment=60):
    logger.info(f'GET {url} {params}')
    attempts = 0
    wait_time = wait_start
    while True:
        if attempts > max_appempts:
            raise Exception(f"Failed to GET {url} {params} after {max_appempts} attempts")
        attempts += 1
        response = requests.get(url, params=params)
        if response.status_code == 429:
            logger.warning(f"Rate limited [{response.status_code}]: sleeping {wait_time} ({attempts}/{max_appempts})")
            time.sleep(wait_time)
            wait_time += wait_increment
        elif response.status_code == 200:
            return response
        else:
            logger.error(f"Error {url}: {response.status_code}: {response.text}")


def get_owned_games(apikey, steamid):
    url = 'http://api.steampowered.com/IPlayerService/GetOwnedGames/v0001/'
    params = {
        'key': apikey,
        'steamid': steamid,
        'format': 'json'
    }
    response = do_get(url, params=params)
    data = response.json()
    assert data['response']['game_count'] == len(data['response']['games'])
    return data['response']['games']


def fetch_game_info(apikey, game_id):
    logger.info(f"Fetching {game_id}...")
    url = 'http://store.steampowered.com/api/appdetails/'
    params = {
        'appids': game_id
    }
    response = do_get(url, params=params)
    data = response.json()
    if not data[str(game_id)]['success']:
        logger.error(f"Failed to fetch game info for appid {game_id}")
        return {}
    return data[str(game_id)]['data']


def check_env():
    steam_id = os.getenv('STEAM_ID', None)
    if not steam_id:
        raise ValueError('STEAM_ID not set')
    apikey = os.getenv('STEAM_APIKEY', None)
    if not apikey:
        raise ValueError('STEAM_APIKEY not set')
    return steam_id, apikey

if __name__ == '__main__':
    steam_id, apikey = check_env()
    steamid = '76561198089811263'
    apikey = '5EFBADA8679541047F7DFC6A0B1B5109'
    games = {}
    if len(sys.argv) < 2:
        logger.warning('Startign from scratch, no games file provided')
    else:
        with open(sys.argv[1], 'r') as file:
            games = json.load(file)

    owned_games = get_owned_games(apikey, steamid)
    try:
        for i, game in enumerate(owned_games):
            logger.info(f"Checking game {i+1}/{len(owned_games)} (appid: {game['appid']})")
            if str(game['appid']) in games:
                logger.info(f"Skipping {game['appid']}, already fetched")
            else:
                fetched_game = fetch_game_info(apikey, game['appid'])
                games[str(game['appid'])] = fetched_game
    finally:
        timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
        new_out_file = f"games.{timestamp}.json"
        logger.info(f"Writing to {new_out_file}")
        with open(new_out_file, 'w') as file:
            json.dump(games, file, indent=4)
