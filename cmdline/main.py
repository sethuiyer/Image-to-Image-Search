import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'  #surpress tensorflow warnings
from capgen import CaptionGenerator
try:
	from query import description_search
except:
	print('Please ensure the elastic search server is enabled')
from PIL import Image
c = CaptionGenerator()
import index
import query
PATH_TO_FLICK8K_IMG="imgs/"
while True:
	print('Enter the Image path to get Similar Images ( q to quit)')
	img_path = input()
	if img_path != "q":
		print('Processing Image Caption...')
		caption = c.get_caption(img_path)
		print('The Generated caption for this image is {} .'.format(caption))
		print('Matching Nearest Captions...')
		answers = query.description_search(caption)
		if len(answers) == 0:
			print('No similar images found')
		for _ in range(len(answers)):
			print(PATH_TO_FLICK8K_IMG+answers[_]['URL'])
			img = Image.open(PATH_TO_FLICK8K_IMG+answers[_]['URL'])
			img.show()
	else:
		break

