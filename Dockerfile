FROM python:3

SHELL ["/bin/bash", "-c"]

RUN apt-get update \
	&& apt-get upgrade -y

RUN useradd -m -s /bin/bash hoge \
	&& mkdir /home/hoge/virtualenv \
	&& mkdir /home/hoge/python-ordercrypto \
	&& chown -R hoge /home/hoge/virtualenv /home/hoge/python-ordercrypto

USER hoge
WORKDIR /home/hoge/virtualenv
RUN python3 -m venv bitbankcc \
	&& . bitbankcc/bin/activate \
	&& pip install --upgrade pip \
	&& pip install requests python-dotenv pyyaml pyzipper \
	&& pip install git+https://github.com/bitbankinc/python-bitbankcc@fba9f83\#egg=python-bitbankcc

WORKDIR /home/hoge/python-ordercrypto
COPY --chown=hoge . .

EXPOSE 5555
CMD ./start.sh
