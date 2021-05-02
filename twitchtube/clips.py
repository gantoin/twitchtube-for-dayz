from math import ceil
from json import dump
import urllib.request
import re

from .logging import Log
from .api import get


log = Log()


def get_data(slug: str, oauth_token: str, client_id: str) -> dict:
    """
    Gets the data from a given slug,
    returns a JSON respone from the Helix API endpoint
    """
    response = get("data", slug=slug, oauth_token=oauth_token, client_id=client_id)

    try:
        return response["data"][0]
    except KeyError as e:
        log.error(f"Ran into exception: {e}, {response}")
        return response


def get_clip_data(slug: str, oauth_token: str, client_id: str) -> tuple:
    """
    Gets the data for given slug, returns a tuple first
    entry being the mp4_url used to download the clip,
    second entry being the title of the clip to be used as filename.
    """
    clip_info = get_data(slug, oauth_token, client_id)

    if "thumbnail_url" in clip_info and "title" in clip_info:
        # All to get what we need to return
        # the mp4_url and title of the clip
        thumb_url = clip_info["thumbnail_url"]
        slice_point = thumb_url.index("-preview-")
        mp4_url = thumb_url[:slice_point] + ".mp4"

        return mp4_url, clip_info["title"]

    raise TypeError(
        f"We didn't receieve what we wanted. /helix/clips endpoint gave:\n{clip_info}"
    )


def get_progress(count, block_size, total_size) -> None:
    """
    Used for printing the download progress
    """
    percent = int(count * block_size * 100 / total_size)
    print(f"Downloading clip... {percent}%", end="\r", flush=True)


def get_slug(clip: str) -> str:
    """
    Splits up the URL given and returns the slug
    of the clip.
    """
    slug = clip.split("/")
    return slug[len(slug) - 1]


def download_clip(clip: str, basepath: str, oauth_token: str, client_id: str) -> None:
    """
    Downloads the clip, does not return anything.
    """
    slug = get_slug(clip)
    mp4_url, _ = get_clip_data(slug, oauth_token, client_id)
    # Remove special characters so we can save the video
    regex = re.compile("[^a-zA-Z0-9_]")
    out_filename = regex.sub("", slug) + ".mp4"
    output_path = basepath + "/" + out_filename

    log.clip(f"Downloading clip with slug: {slug}.")
    log.clip(f"Saving '{slug}' as '{out_filename}'.")
    # Download the clip with given mp4_url
    urllib.request.urlretrieve(mp4_url, output_path, reporthook=get_progress)
    log.clip(f"{slug} has been downloaded.\n")


def get_clips(
    category: str,
    name: str,
    path: str,
    seconds: float,
    ids: list,
    client_id: str,
    oauth_token: str,
    period: str,
    language: str,
    limit: int,
) -> (dict, list, list):
    """
    Gets the top clips for given game, returns JSON response
    from the Kraken API endpoint.
    """
    data = {}
    new_ids = []
    new_titles = []

    headers = {"Accept": "application/vnd.twitchtv.v5+json", "Client-ID": client_id}

    params = {"period": period, "limit": limit}
    params[category] = name

    if language:
        params["language"] = language

    response = get("top_clips", headers=headers, params=params)

    if not response.get("clips"):
        if response.get("error") == "Internal Server Error":
            # the error is twitch's fault, we try again
            get_clips(
                category,
                name,
                path,
                seconds,
                ids,
                client_id,
                oauth_token,
                period,
                language,
                limit,
            )

        else:
            log.warn(
                f'Did not find "clips" in response {response} for {category} {name}, period: {period} language: {language}'
            )

    if "clips" in response:
        for clip in response["clips"]:
            duration = clip["duration"]

            if seconds <= 0.0:
                break

            tracking_id = clip["tracking_id"]

            if not tracking_id in ids:
                data[clip["tracking_id"]] = {
                    "url": "https://clips.twitch.tv/" + clip["slug"],
                    "title": clip["title"],
                    "display_name": clip["broadcaster"]["display_name"],
                    "duration": duration,
                }
                new_ids.append(tracking_id)
                new_titles.append(clip["title"])
                seconds -= duration

        return (data, new_ids, new_titles)

    return ({}, [], [])


def download_clips(data: dict, path: str, oauth_token: str, client_id: str) -> list:
    """
    Downloads clips, returns a list of streamer names.
    """
    names = []

    for clip in data:
        download_clip(data[clip]["url"], path, oauth_token, client_id)

        name = data[clip]["display_name"]

        names.append(name)

    log.info(f"Downloaded {len(data)} clips from this batch.\n")
    return names
