cleandb:
	python manage.py sqlclear motsdits | python manage.py dbshell;
	python manage.py syncdb;

assets:
	lessc design/assets/less/motsdits.less design/assets/css/motsdits.css