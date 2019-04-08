
VENV := env

all: clean init run

init: requirements.txt
	virtualenv -p python3 ${VENV}
	. ${VENV}/bin/activate && pip install -r requirements.txt
	
run:
	. ${VENV}/bin/activate; python run.py

clean:
	rm -rf ${VENV}
	find -iname "*.pyc" -delete
