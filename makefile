LESS=design/assets/less
CSS=design/assets/css
JS=design/assets/js

cleandb:
	python manage.py sqlclear motsdits | python manage.py dbshell;
	python manage.py syncdb;

assets:
# Main application css
	lessc $(LESS)/motsdits.less $(CSS)/motsdits.css
	@csso $(CSS)/motsdits.css $(CSS)/motsdits.min.css
# Login page css
	lessc $(LESS)/login.less $(CSS)/login.css
	@csso $(CSS)/login.css $(CSS)/login.min.css