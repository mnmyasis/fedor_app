FROM mnmyasis/fedor:v4
RUN apt update \
	&& apt install doxygen-doc -y \
	&& apt install graphviz -y \
	&& apt install git -y \
	&& apt-get install python3 -y \
	&& apt-get install python3-pip -y && pip3 install --upgrade pip \
	&& cd /home/dev/fedor_app/ \
	&& git init \
	&& git fetch && git checkout dev \
	&& git pull

WORKDIR ./fedor_app

# CMD python3/fedor/manage.py runserver