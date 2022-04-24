from eyed3.id3.frames import ImageFrame
from PIL import Image
import requests
import eyed3
import io
import re
import os
import time
import json
from urllib.parse import quote


CLIENT_ACCESS_TOKEN = os.environ['CLIENT_ACCESS_TOKEN']
upload_folder = 'api/src/uploads/'


def deEmojify(text):

""" remover emoji ou simbolos ocultos do nome da musica."""

    regrex_pattern = re.compile(pattern = "["
        u"\U0001F600-\U0001F64F" 
        u"\U0001F300-\U0001F5FF" 
        u"\U0001F680-\U0001F6FF"  
        u"\U0001F1E0-\U0001F1FF" 
                           "]+", flags = re.UNICODE)
    return regrex_pattern.sub(r'',text)


class MetadataEdit:

	def edit(yt, file):

		def bygeniusapi(song:str, file:str ,album:str):

			tem = None

			try:

				song_replace = song.replace(re.findall("\[.+\]|\(.+\)" , song)[0] , '')
				song = song_replace

			except:

				pass

			song = deEmojify(song)

			music = {

			"song":"",
			"year":"",
			"album":"",
			"artist":"",
			"album_cover":""}

			response = requests.get(f"https://api.genius.com/search?q={quote(song)}&access_token={CLIENT_ACCESS_TOKEN}")

			if response.status_code == 200:

				music_details = json.loads(response.text)
				
				for hit in music_details['response']['hits'] :

						if hit['result']['title'].upper() in file.upper():

							
							music['song'] = hit['result']['title']
							music['artist'] = hit['result']['artist_names']
							music['album_cover'] = hit['result']['song_art_image_url']

							if album == None:

								music['album'] = music['song']

							else:

								music['album'] = album

							audiofile = eyed3.load(upload_folder + file)

							if (audiofile.tag == None):

								audiofile.initTag()

							audiofile.tag.images.set(ImageFrame.FRONT_COVER ,requests.get(music['album_cover']).content , 'image/jpeg')
							audiofile.tag.title = u'{}'.format(music['song'])
							audiofile.tag.album = u'{}'.format(music['album'])
							audiofile.tag.artist = u'{}'.format(music['artist'])
							audiofile.tag.save(version=eyed3.id3.ID3_V2_3)
							tem = True
							return True
							break;

						else:

							tem = False

				if tem == False or tem == None:

					return False

			else:

				print(f'\n[!] a API retornou um erro com codigo : {response.status_code}.\n[!] (API) {response.text}')
				return False


		def bypytube(yt,file):

			uncut_cover = Image.open(io.BytesIO(requests.get(yt.thumbnail_url).content))
			output_cut_cover = io.BytesIO()
			cut_cover = uncut_cover.crop((0, 60, 510, 420))
			cut_cover.save(output_cut_cover, format='JPEG')
			audiofile = eyed3.load(upload_folder + file)

			if (audiofile.tag == None):
			    audiofile.initTag()

			audiofile.tag.images.set(ImageFrame.FRONT_COVER, output_cut_cover.getvalue() , 'image/jpeg')

			try:

			 	audiofile.tag.title = u'{}'.format(yt.metadata[0]['Song'])

			except:

				pass

			try:

			 	audiofile.tag.album = u'{}'.format(yt.metadata[0]['Album'])

			except:

				pass
				
			try:

			 	audiofile.tag.artist = u'{}'.format(yt.metadata[0]['Artist'])

			except:

				pass

			audiofile.tag.save(version=eyed3.id3.ID3_V2_3)
		
		try:

			try:

				album_name = yt.metadata[0]['Album']

			except:
			
				album_name = None

			result = bygeniusapi(song=file.replace(f"({re.findall('([0-9]+kbps)' , file)[0]}).mp3" , '') , file=file , album=album_name)

			if result == False:

				bypytube(yt,file)

		except Exception as errorr:

			print(errorr)
			bypytube(yt, file)