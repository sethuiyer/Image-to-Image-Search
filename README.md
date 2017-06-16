# Image-to-Image-search
* Image-to-Image-search is a reverse image search engine. 
* Search by image: Give it an image and it will return the similar images based on the image captions.
* Uses Deep Learning for Automatic Image Captioning, Elastic search as it's search engine.


### Automatic Image Captioning 
[Click Here](https://www.youtube.com/watch?v=AGdGVddAJJk) if you wish to see the video demo of the Automatic Image Captioning system

## Packages Required:
* Anaconda
* Keras with Tensorflow Backend
* Elastic Search and py-elasticsearch

## Other things which are required
* Flickr-8k LSTM weights (flickr8k\_cnn\_lstm\_v1.p)
* Flickr-8k dataset is required.

## Output
### Input Image

![image](surf.png)

### Output 
<img src="img1.jpg" width="25%"><img src="img2.jpg" width="25%"><img src="img3.jpg" width="25%"><img src="img4.jpg" width="25%">

### Files
* `extract_feat.py` : Takes in image, returns the feature vector of the image
* `capgen.py` : Takes in the feature vector, produces image captions using LSTM (Long Short Term Memory network)
* `index.py` : Parses the `img/` folder, indexes images and their descriptions in the elastic search server
* `query.py` : Given a description, returns nearest description and their image path as JSON response.
* `main.py` : Main program, elastic search server must be running before launching this program.

## Possible Improvements
* Usage of Flickr 30k dataset
* Using Beam search while generating descriptions

## TODO:
* Making this as web application
