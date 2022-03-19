import requests
import eyed3
from eyed3.id3.frames import ImageFrame
from PIL import Image
import io


upload_folder = 'api/src/uploads/'

import eyed3

def metadataEditAudio(yt, file):

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