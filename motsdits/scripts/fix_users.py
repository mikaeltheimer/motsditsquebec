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

    print "You now have to manually update the auth_user constraints below:"
    cursor.execute("show create table motsdits_photo_likes")
    print iter(cursor).next()
    raw_input("alter table motsdits_photo_likes drop foreign key {0}".format(raw_input("constraint id> ")))
    cursor.execute("alter table motsdits_photo_likes add constraint `user_id_refs_user_new` FOREIGN KEY (`user_id`) REFERENCES `motsdits_user` (`id`);")

    cursor.execute("show create table motsdits_opinion_approvals")
    print iter(cursor).next()
    raw_input("alter table motsdits_opinion_approvals drop foreign key {0}".format(raw_input("constraint id> ")))
    cursor.execute("alter table motsdits_opinion_approvals add constraint `user_id_refs_user_opinion` FOREIGN KEY (`user_id`) REFERENCES `motsdits_user` (`id`);")

    cursor.execute("show create table motsdits_opinion_dislikes")
    print iter(cursor).next()
    raw_input("alter table motsdits_opinion_dislikes drop foreign key {0}".format(raw_input("constraint id> ")))
    cursor.execute("alter table motsdits_opinion_dislikes add constraint `user_id_opinion_dislike` FOREIGN KEY (`user_id`) REFERENCES `motsdits_user` (`id`);")

    cursor.execute("show create table motsdits_motdit_recommendations")
    print iter(cursor).next()
    cursor.execute("alter table motsdits_motdit_recommendations drop foreign key {0}".format(raw_input("constraint id> ")))
    cursor.execute("alter table motsdits_motdit_recommendations add constraint `user_id_recommend` FOREIGN KEY (`user_id`) REFERENCES `motsdits_user` (`id`);")
