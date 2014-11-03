import mechanize
import re
from datetime import datetime
import random

recommend_list = ["Love this track! check it out!",
				  "Kind of cheesy but check it out anyway ;)",
				  "Just listen to this beat,",
				  "Love it!",
				  "Really like this one,",
				  "Awesome,",
				  "Killing it!",
				  "Big LIKE!",
				  "This is just out!",
				  "One track a day, keeps the doctor away:",
				  "Superb!!!",
				  "Check it out!",
				  "The one track you should listen to... Right here ->",
				  "Oh my, sweet music!"
				]

user_names = ["thesoundyouneed1",
			  "majesticcasual",
			  "nprmusic",
			  "pitchforktv",
			  "LaBelleChannel",
			  "chillmasterschannel",
			  "xibuprofenx",
			  "wildsoundscivilised",
			  "tragicclothing",
			  "DelicieuseMusique",
			  "MyEssentialsMusic"
			]

def get_tweet_text():
	return "{} {}".format(recommend_list[random.randint(0,len(recommend_list)-1)],
		   get_random_video_from_today())

def get_random_video_from_today():
	links = [get_newest_video_link(user) for user in user_names]
	dates = [get_upload_date(link) for link in links]

	videos = []
	for i in enumerate(links):
		videos.append([links[i[0]],dates[i[0]]])

	newest = [video for video in videos if _is_today(video[1])]
	
	if not newest:
		return "No videos from today"
	else:
		return newest[random.randint(0,len(newest)-1)][0]		

def get_newest_video_link(youtube_user_name):
	youtube = "https://www.youtube.com/user/" + youtube_user_name + "/videos"

	b = mechanize.Browser()
	html_page = b.open(youtube)
	html_text = html_page.read()

	vid_meta = re.search('<h3 class="yt-lockup-title">.*?</h3>',html_text)
	vid_link = vid_meta.group()

	link = _clean_string(vid_link, 'href="', '&amp;')
	b.close()
	return "http://www.youtube.com" + link



def get_upload_date(url):
	b = mechanize.Browser()
	html_page = b.open(url)
	html_text = html_page.read()

	vid_meta = re.search('class="watch-time-text">.*?</strong>',html_text)
	vid_date = vid_meta.group()

	date = _clean_string(vid_date, 'class="watch-time-text">Published on ',
						'</strong>')
	b.close()

	return _convert_youtube_date_to_datetime(date)

def _clean_string(meta, start, end):
	clean_exp = start + ".*?" + end
	text = re.search(clean_exp,meta)
	text = text.group()
	text = re.sub(start, '', text)
	text = re.sub(end, '', text)

	return text

def _is_today(date):
	present = datetime.today()
	today = datetime(year=present.year, 
					 month=present.month, 
					 day=present.day)

	if date >= today:
		return True
	else:
		return False

def _convert_youtube_date_to_datetime(youtube_date):
    """
....English (US) lang
...."""

    months = {
        'Jan': 1,
        'Feb': 2,
        'Mar': 3,
        'Apr': 4,
        'May': 5,
        'Jun': 6,
        'Jul': 7,
        'Aug': 8,
        'Sep': 9,
        'Oct': 10,
        'Nov': 11,
        'Dec': 12,
    }
    date = date.split()
    year = int(date[2])
    month = int(months[date[0]])
    day = int(date[1].strip(','))

    return datetime(
        year,
        month,
        day
    )


# def _convert_youtube_date_to_datetime(youtube_date):
#     """
# ....Danish lang
# ...."""
#     date = re.split('/', youtube_date)

#     if date[0].startswith('0'):
#         day = int(date[0][1:])
#     else:
#         day = int(date[0])

#     if date[1].startswith('0'):
#         month = int(date[1][1:])
#     else:
#         month = int(date[1])

#     year = int(date[2])
    
#     return datetime(
#         year,
#         month,
#         day,
#     )


# execfile("youtube_extractor.py")