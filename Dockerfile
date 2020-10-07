FROM ubuntu
RUN apt update \
	&& apt install doxygen-doc -y \
	&& apt install graphviz -y \
	&& apt install git -y \
	&& apt-get install python3 -y \
	&& apt-get install python3-pip -y && pip3 install --upgrade pip \
	&& cd home \
	&& mkdir fedor_app \
	&& cd fedor_app \

WORKDIR ./fedor_app

CMD python3/fedor/manage.py runserver