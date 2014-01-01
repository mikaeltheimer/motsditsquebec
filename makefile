LESS=design/assets/less
CSS=design/assets/css
JS=design/assets/js

all:

# Loads all fixture files
ldfixtures:
	python manage.py loaddata motsdits/fixtures/*

# Creates all necessary fixture files
mkfixtures:
	python manage.py dumpdata auth.User --indent 4 > motsdits/fixtures/auth-users.json
	python manage.py dumpdata motsdits --indent 4 > motsdits/fixtures/test-data.json

cleandb:
	echo 'drop database motsdits; create database motsdits;' | python manage.py dbshell;
	python manage.py syncdb;

assets:
# Main application css
	lessc $(LESS)/application.less $(CSS)/application.css
	@csso $(CSS)/application.css $(CSS)/application.min.css
# Login page css
	lessc $(LESS)/login.less $(CSS)/login.css
	@csso $(CSS)/login.css $(CSS)/login.min.css
# Single mot-dit page css
	lessc $(LESS)/motdit.less $(CSS)/motdit.css
	@csso $(CSS)/motdit.css $(CSS)/motdit.min.css
# Grid css
	lessc $(LESS)/grid.less $(CSS)/grid.css
	@csso $(CSS)/grid.css $(CSS)/grid.min.css
# CSS for profile
	lessc $(LESS)/includes/profile.less $(CSS)/profile.css
	@csso $(CSS)/profile.css $(CSS)/profile.min.css
# Edit page css
	lessc $(LESS)/edit-motdit.less $(CSS)/edit-motdit.css
	@csso $(CSS)/edit-motdit.css $(CSS)/edit-motit.min.css
# Modal custom css
	lessc $(LESS)/form-modal.less $(CSS)/form-modal.css
	@csso $(CSS)/form-modal.css $(CSS)/form-modal.min.css

# Creates a usable requirements file
requirements:
	pip freeze | sed -e '/git-remote-helpers/ d' > requirements.txt
