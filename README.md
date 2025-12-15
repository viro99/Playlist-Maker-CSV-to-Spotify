# Spotify Playlist Maker from CSV

This tool reads a CSV file containing artist names and automatically creates a Spotify playlist with their most popular tracks.

## Features

- Reads artists from a CSV file
- Fetches the top 5 most popular tracks for each artist from Spotify
- Creates a new Spotify playlist with all collected tracks
- Provides detailed logging and error reporting
- Handles artists that can't be found on Spotify gracefully

## Prerequisites

- Python 3.6 or higher
- A Spotify account
- Spotify Developer App credentials

## Spotify Developer Setup

1. Go to [Spotify Developer Dashboard](https://developer.spotify.com/dashboard/applications)
2. Click "Create an App"
3. Fill in the app details:
   - **App name**: Something like "Playlist Maker"
   - **App description**: "Creates playlists from CSV artist lists"
   - **Redirect URI**: `http://127.0.0.1:8080`
4. Copy your **Client ID** and **Client Secret** - you'll need them to run the script

## Installation

1. Clone or download this repository
2. Create a virtual environment:
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

1. Place your CSV file in the same directory as the script
   - The CSV should have a header row (e.g., "Artist Name")
   - Each subsequent row should contain one artist name

2. (Optional) Create `spotify_credentials.txt` for convenience:
   ```
   Client ID: your_client_id_here
   Client Secret: your_client_secret_here
   ```
   This file is automatically ignored by git for security.

3. Run the script:
   ```bash
   python playlist_maker.py
   ```

4. If credentials weren't in the file, you'll be prompted to enter:
   - Spotify Client ID
   - Spotify Client Secret

4. The script will open a browser window for Spotify authentication
   - Log in to Spotify if prompted
   - Authorize the app to create playlists

5. The script will process each artist and create your playlist

## Output

The script provides detailed output including:
- Authentication confirmation
- Number of artists found in CSV
- Processing status for each artist
- Final success message with playlist URL

## Example CSV Format

```
Artist Name
Empire of the Sun
Mau P
Sara Landry
Zeds Dead
```

## Troubleshooting

### Artist Not Found
- Check for typos in artist names
- Some artists may not be available on Spotify or have different names
- The script will skip unfound artists and continue

### Authentication Issues
- Verify your Client ID and Client Secret are correct
- Ensure the Redirect URI in your Spotify app matches `http://127.0.0.1:8080`
- Try clearing your browser cache for Spotify authentication

### Rate Limiting
- The script includes delays to avoid hitting Spotify API limits
- If you have many artists, it may take some time to complete

## License

This project is for educational purposes. Please ensure your usage complies with Spotify's Terms of Service.

## Support

If you encounter issues, check the console output for error messages and verify your setup against the instructions above.
