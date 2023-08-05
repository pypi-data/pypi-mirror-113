import requests, json, datetime

def getupc(upc):
  link = f"https://api.deezer.com/album/upc:" + upc
  response = requests.get(link).text
  data = json.loads(response)
  artist = data["artist"]["name"]
  title = data["title"]
  date = data["release_date"]
  label = data["label"]
  kol_track = data["nb_tracks"]
  result = f"{artist} - {title}\n\nUPC: {upc}\nДата релиза: {date}\nЛейбл: {label}\n\nКоличество треков: {kol_track}"
  return result
  
def getisrc(isrc):
	link = f"https://api.deezer.com/track/isrc:" + isrc
	response = requests.get(link).text
	data = json.loads(response)
	track_id = data["id"]
	artist = data["artist"]["name"]
	title = data["album"]["title"]
	date = data["release_date"]	
	track_link = data["link"]
	duration = data["duration"]
	cover = data["album"]["cover_xl"]
	dur = str(datetime.timedelta(seconds=duration))
	result = f"{artist} - {title}\n\nISRC: {isrc}\nДата релиза: {date}\nДлительность: {dur}\nСсылка на Deezer - {track_link}"
	return result
