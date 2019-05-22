FROM fedora:30

EXPOSE 5000

RUN dnf -y -q -b install python3-virtualenv npm

ADD . /app
RUN cd app && virtualenv-3.4 .
RUN cd app && npm install


RUN bash -c '. app/bin/activate; pip install flask flask-assets requests PyReact'

RUN mkdir -p /app/static/.webassets-cache/
RUN chown nobody /app/static/.webassets-cache/
RUN chmod 700 /app/static/.webassets-cache/

USER nobody

CMD bash -c '. app/bin/activate; python app/test.py'

