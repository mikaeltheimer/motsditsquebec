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
	lessc $(LESS)/single-motdit.less $(CSS)/single-motdit.css
	@csso $(CSS)/single-motdit.css $(CSS)/single-motdit.min.css