from django.db import connection


def run():
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM auth_user")

    from motsdits.models import User
    for pk, password, _, is_superuser, username, first, last, email, is_staff, is_active, _ in cursor:
        user = User.objects.get_or_create(pk=pk, defaults={
            'password': password,
            'is_superuser': is_superuser,
            'username': username,
            'first_name': first,
            'last_name': last,
            'email': email,
            'is_staff': is_staff,
            'is_active': is_active
        })

        print user
