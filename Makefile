.PHONY: run clean requirements install pylint jslint lint deploy

run:
	# requires APP_SETTINGS=config.[ProductionConfig|StagingConfig|DevelopmentConfig|TestingConfig]
	# and DATABASE_URL="xxx"
	python manage.py runserver

clean:
	find . -type f -name '*.py[cod]' -delete
	find . -type f -name '*.*~' -delete

requirements:
	pip install -r requirements.txt

install: clean requirements env

pylint:
	-flake8 .

jslint:
	-jshint -c .jshintrc --exclude-path .jshintignore .

lint: clean pylint jslint

deploy: lint
	git push heroku master
