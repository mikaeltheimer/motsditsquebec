LESS=design/assets/less
CSS=design/assets/css
JS=design/assets/js

cleandb:
	python manage.py sqlclear motsdits | python manage.py dbshell;
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
# Edit page css
	lessc $(LESS)/edit-motdit.less $(CSS)/edit-motdit.css
	@csso $(CSS)/edit-motdit.css $(CSS)/edit-motdit.min.css

# Creates a usable requirements file
requirements:
	pip freeze | sed -e '/git-remote-helpers/ d' > requirements.txt
