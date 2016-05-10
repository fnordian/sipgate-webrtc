FROM fedora:latest

EXPOSE 5000

RUN dnf -y -q -b install python3-virtualenv npm

ADD . /app
RUN cd app && virtualenv-3.4 .
RUN cd app && npm install jssip

RUN bash -c '. app/bin/activate; pip install flask requests'

USER nobody

CMD bash -c '. app/bin/activate; python app/test.py'

