FROM mnmyasis/fedor:v4
RUN apt update \
	&& apt install doxygen-doc -y \
	&& apt-get install language-pack-ru -y \
	&& update-locale LANG=ru_RU.UTF-8 \
	&& apt install graphviz -y \
	&& apt install git -y \
	&& apt-get install python3 -y \
	&& apt-get install python3-pip -y && pip3 install --upgrade pip \
	&& pip3 install -r requirements.txt 

WORKDIR /home/

#CMD service postgresql start
#CMD python3 fedor/manage.py runserver 0.0.0.0:8000