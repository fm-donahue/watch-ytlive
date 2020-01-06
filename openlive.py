#! python3
# Opens a new tab for one of your favorite youtuber livestream

import os
import time
import webbrowser

import requests


chrome_path = "C:\\Program Files (x86)\\Google\\Chrome\\Application\\chrome.exe"
webbrowser.register('chrome', None, webbrowser.BackgroundBrowser(chrome_path))


def look_for_live_stream():
    api_key = os.environ.get('youtube_api_key')
    channel_id = 'UC-sJ8u8eu_ivfzekwkue38g'

    base_url_video = 'https://www.youtube.com/watch?v='
    base_search_url = 'https://www.googleapis.com/youtube/v3/search?'

    url = base_search_url + f'part=snippet&channelId={channel_id}&eventType=live&type=video&key={api_key}'

    # Contact api
    response = requests.get(url)

    try:
        response.raise_for_status()
    except Exception as exc:
        print(f'There was a problem: {exc}')
        return

    video_data = response.json()

    # Open youtube video on browser
    if video_data['items'] != []:
        video_id = video_data['items'][0]['id']['videoId']
        webbrowser.get('chrome').open_new_tab(base_url_video +
                                              video_id)


try:
    while True:
        look_for_live_stream()
        time.sleep(60)
except KeyboardInterrupt:
    print('\n\nStop')
