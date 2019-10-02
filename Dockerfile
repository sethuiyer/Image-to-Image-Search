FROM ubuntu:16.04
RUN apt-get update
RUN apt-get install -y apt-utils
RUN apt-get install -y curl
RUN apt-get install -y wget
RUN apt-get install -y vim
RUN apt-get install -y git-core
RUN apt-get install -y python3
RUN curl -O https://bootstrap.pypa.io/get-pip.py
RUN python3 get-pip.py
RUN rm get-pip.py
RUN git clone -b docker_image https://github.com/sethuiyer/Image-to-Image-Search.git /image_search
RUN pip3 install -r /image_search/requirements.txt
RUN wget https://cs.stanford.edu/people/karpathy/neuraltalk/flickr8k_cnn_lstm_v1.zip
RUN apt-get install -y unzip
RUN unzip flickr8k_cnn_lstm_v1.zip
RUN rm flickr8k_cnn_lstm_v1.zip
RUN mv *.p /image_search/models/
CMD ["python3","/image_search/server.py"]
EXPOSE 5000



