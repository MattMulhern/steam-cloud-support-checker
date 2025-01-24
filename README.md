
## Description
Some scripts to query steam api for Steam Cloud Save Support.

## Dependencies
```
pip install -r requirements.txt
```

## Usage
1. Set the environment variables `STEAM_ID` and `STEAM_APIKEY` with your Steam ID and API key.
2. Fetch the list of owned games and their details:
    ```sh
    python3 get_games.py
    ```
    (optional) supply a json file of games to read (for resuming previous runs)
    ```sh
    python3 get_games.py ./games.json
    ```
3. Check which games support Steam Cloud:
    ```sh
    python check_cloud_support.py games.<timestamp>.json
    ```

## License
This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
