FROM ubuntu
RUN apt update \
	&& apt install doxygen-doc -y \
	&& apt install graphviz -y \
	&& apt install git -y \
	&& apt-get install python3 -y \
	&& apt-get install python3-pip -y && pip3 install --upgrade pip \
	&& cd home \
	&& mkdir dev \
	&& cd dev \
	&& yes |git clone git@bitbucket.org:mnmyasis1/fedor_app.git

WORKDIR ./fedor_app

# CMD python3/fedor/manage.py runserver