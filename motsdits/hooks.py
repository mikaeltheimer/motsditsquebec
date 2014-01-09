from django.contrib.contenttypes.models import ContentType
from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from motsdits import models, signals
from django.core.exceptions import ValidationError


def ensure_http(url):
    '''Ensures a URL starts with the protocol string'''
    if not url.startswith('http'):
        url = 'http://{url}'.format(url=url)
    return url


@receiver(pre_save, sender=models.User)
def format_twitter(sender, instance, *args, **kwargs):
    '''Formats a user twitter handle as a URL'''
    if instance.twitter:

        # Check for @user
        if instance.twitter.startswith('@'):
            instance.twitter = 'twitter.com/{handle}'.format(handle=instance.twitter[1:])
        elif not 'twitter' in instance.twitter and '/' in instance.twitter:
            raise ValidationError("Twitter handles must either be a username or a full url")

        instance.twitter = ensure_http(instance.twitter)


@receiver(pre_save, sender=models.User)
def format_facebook(sender, instance, *args, **kwargs):
    '''Ensures the facebook url is in the right format'''
    if instance.facebook:
        instance.facebook = ensure_http(instance.facebook)


@receiver(pre_save, sender=models.User)
def format_website(sender, instance, *args, **kwargs):
    '''Ensures the website url is in the right format'''
    if instance.website:
        instance.website = ensure_http(instance.website)


def add_activity(activity_type, instance, created_by):
    '''Adds an activity object for the supplied instance'''
    try:
        instance_type = ContentType.objects.get_for_model(instance)
        models.Activity.objects.get(content_type__pk=instance_type.id, object_id=instance.id, activity_type=activity_type)
    except models.Activity.DoesNotExist:
        models.Activity(
            content_object=instance,
            activity_type=activity_type,
            created_by=created_by
        ).save()


@receiver(post_save, sender=models.MotDit)
def create_motdit_activity(sender, instance, *args, **kwargs):
    '''Ensures the motdit created activity gets created'''
    if not instance.id:
        return add_activity('motdit-add', instance, instance.created_by)


@receiver(signals.motdit_recommended)
def recommend_motdit_activity(sender, motdit=None, *args, **kwargs):
    '''Creates a "user favourited motdit" activity
    @TODO: what happens when we un-recommend a mot-dit'''
    print "ACTIVITY RECOMMEND"
    return add_activity('motdit-favourite', motdit, sender)


@receiver(signals.motdit_comment)
def comment_motdit_activity(sender, instance=None, opinion=None, *args, **kwargs):
    '''Creates a "user commented on motdit" activity'''
    print "Activity!"
    return add_activity('motdit-comment', opinion, sender)


@receiver(signals.photo_like)
def like_photo_activity(sender, instance=None, photo=None, *args, **kwargs):
    '''Creates a "user liked photo" activity
    @TODO: what happens when we un-like a photo'''
    return add_activity('photo-like', photo, sender)