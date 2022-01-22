import pathlib
from datetime import date

# Note:
# Changing FRAMES and or RESOLUTION will heavily impact load on CPU.
# If you have a powerful enough computer you may set it to 1080p60

# other
PATH = str(pathlib.Path().absolute()).replace("\\", "/")
CLIP_PATH = PATH + "/clips/{}/{}"
CHECK_VERSION = True  # see if you're running the latest versions
DEBUG = True  # If additional/debug information should be printed (True/False)

DATA = ["g DayZ"]
BLACKLIST = [
    "c BibixHD"
]  # channels/games you dont want to be included in the video

# twitch
CLIENT_ID = ""  # Twitch Client ID
OAUTH_TOKEN = ""  # Twitch OAuth Token
PERIOD = 72  # how many hours since the clip's creation should've passed e.g. 24, 48 etc 0 for all time
LANGUAGE = ""  # en, es, th etc.
LIMIT = 100  # 1-100

# selenium
ROOT_PROFILE_PATH = "/Users/antoinegauthier/Library/Application Support/Firefox/7wtbtw0r.Selenium"  # Path to the Firefox profile where you are logged into YouTube
EXECUTABLE_PATH = r"geckodriver"
SLEEP = 3  # How many seconds Firefox should sleep for when uploading
HEADLESS = True  # If True Firefox will be hidden (True/False)

# video options
RENDER_VIDEO = True  # If clips should be rendered into one video (True/False). If set to False everything else under Video will be ignored
RESOLUTION = (
    720,
    1280,
)  # Resolution of the rendered video (height, width) for 1080p: ((1080, 1920))
FRAMES = 30  # Frames per second (30/60)
VIDEO_LENGTH = 10.5  # Minimum video length in minutes (doesn't always work)
RESIZE_CLIPS = True  # Resize clips to fit RESOLUTION (True/False) If any RESIZE option is set to False the video might end up having a weird resolution
FILE_NAME = "rendered"  # Name of the rendered video
ENABLE_INTRO = True  # Enable (True/False)
RESIZE_INTRO = True  # Resize (True/False) read RESIZE_CLIPS
INTRO_FILE_PATH = PATH + "/twitchtube/files/intro.mp4"  # Path to video file (str)
ENABLE_TRANSITION = True
RESIZE_TRANSITION = True
TRANSITION_FILE_PATH = PATH + "/twitchtube/files/transition.mp4"
ENABLE_OUTRO = True
RESIZE_OUTRO = True
OUTRO_FILE_PATH = PATH + "/twitchtube/files/outro.mp4"

# other options
SAVE_TO_FILE = True  # If YouTube stuff should be saved to a separate file e.g. title, description & tags (True/False)
SAVE_FILE_NAME = "youtube"  # Name of the file YouTube stuff should be saved to
UPLOAD_TO_YOUTUBE = True  # If the rendered video should be uploaded to YouTube after rendering (True/False)
DELETE_CLIPS = True  # If the downloaded clips should be deleted after rendering the video (True/False)

BEFORE = "Thanks for watching!\n#ZappingDayZ "
today = date.today()

# youtube
TITLE = f"Zapping DayZ (" + '%02d' % today.day + "/" + '%02d' % today.month + "/" + str(
    today.year) + ")"  # youtube title, leave empty for the first clip's title
DESCRIPTION = BEFORE + "#DayZ #Zapping\n"

THUMBNAIL = PATH + "/assets/thumbs/game.png"
TAGS = ["dayz", "dayz pvp", "dayz standalone", "best of dayz", "dayz funny moments", "dayz gameplay", "dayz 2021",
        "dayz ps4", "funny dayz", "dayz standalone gameplay", "dayz twitch", "toperec dayz", "dayz 1.0", "dayz 2022",
        "dayz m1ndr", "dayz (video game)", "dayz xbox one", "dayz standalone update", "dayz memorable moments",
        "dayz xbox", "dayz standalone series", "dayz movie", "dayz beta", "dayz standalone pvp", "dayz hunting bandits",
        "dayz console", "dayz pc", "dayz ps5", "dayz pvp besto of", "dayz m1ndr twitch"
        ]  # your youtube tags
