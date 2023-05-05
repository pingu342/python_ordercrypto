FROM alpine

SHELL ["/bin/sh", "-c"]

RUN apk --no-cache --no-progress upgrade \
	&& apk --no-cache --no-progress add bash tor git python3 py3-pip

SHELL ["/bin/bash", "-c"]

RUN adduser -D -h /home/hoge -s /bin/bash hoge \
	&& echo "DataDirectory /var/lib/tor" >> /etc/tor/torrc \
	&& echo "Log notice file /var/log/tor/notices.log" >> /etc/tor/torrc \
	&& echo "HiddenServiceDir /var/lib/tor/hidden_service" >> /etc/tor/torrc \
	&& echo "HiddenServicePort 80 127.0.0.1:5555" >> /etc/tor/torrc \
	&& mkdir /var/lib/tor/hidden_service \
	&& chown -R hoge /var/lib/tor/hidden_service /var/lib/tor /var/log/tor \
	&& chmod 700 /var/lib/tor/hidden_service \
	&& mkdir /home/hoge/data \
	&& mkdir /home/hoge/virtualenv \
	&& mkdir /home/hoge/python-ordercrypto \
	&& chown -R hoge /home/hoge/data /home/hoge/virtualenv /home/hoge/python-ordercrypto

USER hoge
WORKDIR /home/hoge/virtualenv
RUN python3 -m venv bitbankcc \
	&& . bitbankcc/bin/activate \
	&& pip3 install requests python-dotenv pyyaml pyzipper \
	&& pip3 install git+https://github.com/bitbankinc/python-bitbankcc@fba9f83\#egg=python-bitbankcc

WORKDIR /home/hoge/python-ordercrypto
COPY --chown=hoge . .

EXPOSE 5555
VOLUME /home/hoge/data
ENV ENV_ORDERCRYPTO_DATA_DIR=/home/hoge/data
CMD ./start.sh
#CMD bash
