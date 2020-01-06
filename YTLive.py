#! python3
# This program watches your favorite Youtuber livestream events
# then opens a new tab on your default browser for the video

import datetime
import os
import sys
import time
import webbrowser

import requests

date_today = datetime.date.today()
upcoming_video_exists = start_time = live_stream_starts = False
upcoming_video_data = video_id = ''


def look_for_live_stream():
    global upcoming_video_exists, start_time, live_stream_starts,\
           upcoming_video_data, video_id

    # Get api key at 'https://console.developers.google.com'
    api_key_url = '&key=' + os.environ.get('youtube_api_key')

    # Youtube channel id
    channel_id = 'UC-sJ8u8eu_ivfzekwkue38g'

    base_url_video = 'https://www.youtube.com/watch?v='
    base_url = 'https://www.googleapis.com/youtube/v3/'

    # Check upcoming livestream video
    if not upcoming_video_exists:
        upcoming_live_url = base_url + f'search?part=snippet&channelId={channel_id}\
&eventType=upcoming&publishedAfter={date_today.year}-{date_today.month}\
-{date_today.day}T00%3A00%3A00Z&type=video' + api_key_url

        # Contact api for upcoming livestream
        resp_upcoming = requests.get(upcoming_live_url)

        resp_status = check_status(resp_upcoming)
        if not resp_status:
            return 60

        upcoming_video_data = resp_upcoming.json()

        if upcoming_video_data['items'] != []:
            # Get upcoming live video id
            video_id = upcoming_video_data['items'][0]['id']['videoId']
            upcoming_video_exists = True

        else:
            return 3600

    # Get start time
    live_details_url = base_url + f'videos?part=liveStreamingDetails&\
id={video_id}' + api_key_url

    # Contact api for livestreaming details
    resp_live_details = requests.get(live_details_url)

    resp_status = check_status(resp_live_details)
    if not resp_status:
        return 60

    live_details_data = resp_live_details.json()

    # Get livestream start time
    start_time_json = live_details_data['items'][0]['liveStreamingDetails']['scheduledStartTime']
    start_time = datetime.datetime.strptime(start_time_json,
                                            '%Y-%m-%dT%H:%M:%S.%fZ')

    # Calculate the time left before stream starts
    time_now = datetime.datetime.utcnow()
    time_left = start_time - time_now - datetime.timedelta(seconds=600)

    if time_left.days > -1 and time_left.seconds > 0:
        return time_left.seconds

    search_live_url = base_url + f'search?part=snippet&channelId={channel_id}&\
eventType=live&type=video' + api_key_url

    # Contact api if livestream is starting
    resp_live_video = requests.get(search_live_url)

    resp_status = check_status(resp_live_video)
    if not resp_status:
        return 60

    live_video_data = resp_live_video.json()

    # Open youtube livestream on a new tab
    if live_video_data['items'] != []:
        webbrowser.open_new_tab(base_url_video + video_id)
        live_stream_starts = True
        return 0

    else:
        return 10


def check_status(response):
    try:
        response.raise_for_status()
    except Exception as exc:
        print(f'There was a problem: {exc}')
        print(response.json())
        return False
    return True


print("Watching your favorite Youtuber's Live Events")

try:
    while True:
        while live_stream_starts:
            date_now = datetime.date.today()

            # Restarts the program
            if date_now.day == date_today.day + 1:
                os.execl(sys.executable, sys.executable)

        sleep_time = look_for_live_stream()
        time.sleep(sleep_time)

except KeyboardInterrupt:
    print('\n\nStop')
