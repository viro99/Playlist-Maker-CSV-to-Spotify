#!/usr/bin/env python3
"""
Spotify Playlist Maker from CSV Artist List

This script reads a CSV file containing artist names and creates a Spotify playlist
with their most popular tracks.
"""

import csv
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from datetime import datetime

def main():
    print("Spotify Playlist Maker")
    print("=" * 50)

    # Configuration
    CLIENT_ID = input("Enter your Spotify Client ID: ").strip()
    CLIENT_SECRET = input("Enter your Spotify Client Secret: ").strip()
    REDIRECT_URI = 'http://localhost:8080'  # Must match Spotify app settings

    CSV_FILE = 'Copy of LIB 2026 lineup - Sheet3.csv'

    # Replace with your playlist name and description
    PLAYLIST_NAME = 'LIB 2026 Artist Playlist'
    PLAYLIST_DESCRIPTION = f'Created on {datetime.now().strftime("%Y-%m-%d")} from artist CSV'

    # Authentication
    print("\nAuthenticating with Spotify...")
    scope = "playlist-modify-public playlist-modify-private"
    sp_oauth = SpotifyOAuth(
        client_id=CLIENT_ID,
        client_secret=CLIENT_SECRET,
        redirect_uri=REDIRECT_URI,
        scope=scope
    )

    sp = spotipy.Spotify(auth_manager=sp_oauth)

    # Get user info to confirm authentication
    user = sp.current_user()
    if user:
        print(f"✓ Authenticated as: {user['display_name']} ({user['id']})")
    else:
        print("✗ Authentication failed. Check your credentials and try again.")
        return

    # Read artists from CSV
    print("\nReading artists from CSV...")
    artists = []
    try:
        with open(CSV_FILE, 'r', encoding='utf-8') as file:
            reader = csv.reader(file)
            header = next(reader)  # Skip header row
            for row in reader:
                if row:  # Skip empty rows
                    artists.append(row[0].strip())
        print(f"✓ Found {len(artists)} artists in CSV")
    except FileNotFoundError:
        print(f"✗ CSV file '{CSV_FILE}' not found in current directory")
        return
    except Exception as e:
        print(f"✗ Error reading CSV: {e}")
        return

    # Get top tracks for each artist
    print("\nFetching top tracks from Spotify...")
    track_uris = []
    not_found_artists = []

    for i, artist_name in enumerate(artists, 1):
        print(f"  Processing {i}/{len(artists)}: {artist_name}")
        try:
            # Search for artist
            results = sp.search(q=f'artist:{artist_name}', type='artist', limit=1)
            if results['artists']['items']:
                artist = results['artists']['items'][0]
                artist_id = artist['id']

                # Get top tracks (popularity-based)
                top_tracks = sp.artist_top_tracks(artist_id, country='US')
                if top_tracks['tracks']:
                    # Take top 5 tracks
                    tracks_to_add = top_tracks['tracks'][:5]
                    uris = [track['uri'] for track in tracks_to_add]
                    track_uris.extend(uris)
                    print(f"    ✓ Added {len(uris)} tracks from {artist['name']}")
                else:
                    not_found_artists.append(f"{artist_name} (no tracks found)")
                    print("    ✗ No tracks found")
            else:
                not_found_artists.append(artist_name)
                print("    ✗ Artist not found on Spotify")
        except Exception as e:
            not_found_artists.append(artist_name)
            print(f"    ✗ Error: {str(e)}")

        # Avoid rate limiting
        import time
        time.sleep(0.1)

    # Create playlist
    print(f"\nCreating playlist '{PLAYLIST_NAME}'...")
    print(f"Expected to add {len(track_uris)} tracks")
    # Limit description if too long
    desc = PLAYLIST_DESCRIPTION
    if len(desc) > 300:
        desc = desc[:297] + "..."

    playlist = sp.user_playlist_create(
        user['id'],
        PLAYLIST_NAME,
        public=True,
        description=desc
    )

    if playlist:
        playlist_id = playlist['id']
        print("✓ Playlist created successfully!")
        # Add tracks to playlist
        print("Adding tracks...")
        # Spotify allows adding up to 100 tracks at once
        for i in range(0, len(track_uris), 100):
            batch = track_uris[i:i+100]
            sp.playlist_add_items(playlist_id, batch)
            print(f"  Added {len(batch)} tracks")
    else:
        print("✗ Failed to create playlist")
        return

    # Final summary
    print("\n" + "=" * 50)
    print("✓ PLAYLIST CREATED SUCCESSFULLY!")
    print(f"  Name: {PLAYLIST_NAME}")
    print(f"  Total tracks: {len(track_uris)}")
    print(f"  Spotify URL: {playlist['external_urls']['spotify']}")
    print(f"  Artists processed: {len(artists)}")
    if not_found_artists:
        print(f"  Artists not found/skipped: {len(not_found_artists)}")
        print("  These artists could not be found on Spotify:")
        for artist in not_found_artists[:5]:  # Show first 5
            print(f"    - {artist}")
        if len(not_found_artists) > 5:
            print(f"    ... and {len(not_found_artists) - 5} more")
    print("=" * 50)

if __name__ == "__main__":
    main()
