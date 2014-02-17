from django.db.models.signals import pre_save
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


def add_activity(activity_type, created_by=None, motdit=None, opinion=None, photo=None):
    '''Adds an activity object for the supplied instance'''
    try:
        models.Activity.objects.get(motdit=motdit, opinion=opinion, created_by=created_by, activity_type=activity_type)
    except models.Activity.DoesNotExist:
        models.Activity(
            motdit=motdit,
            opinion=opinion,
            photo=photo,
            activity_type=activity_type,
            created_by=created_by
        ).save()


@receiver(pre_save, sender=models.MotDit)
def create_motdit_activity(sender, instance, *args, **kwargs):
    '''Ensures the motdit created activity gets created'''
    if not instance.id:
        try:
            models.Activity.objects.get(activity_type='motdit-add', motdit=instance)
        except models.Activity.DoesNotExist:
            return add_activity('motdit-add', motdit=instance, created_by=instance.created_by)


@receiver(signals.motdit_recommended)
def recommend_motdit_activity(sender, motdit=None, *args, **kwargs):
    '''Creates a "user favourited motdit" activity
    @TODO: what happens when we un-recommend a mot-dit'''
    return add_activity('motdit-favourite', motdit=motdit, created_by=sender)


@receiver(signals.motdit_comment)
def comment_motdit_activity(sender, instance=None, opinion=None, *args, **kwargs):
    '''Creates a "user commented on motdit" activity'''
    return add_activity('motdit-comment', opinion=opinion, motdit=opinion.motdit, created_by=sender)


@receiver(signals.photo_like)
def like_photo_activity(sender, instance=None, photo=None, *args, **kwargs):
    '''Creates a "user liked photo" activity
    @TODO: what happens when we un-like a photo'''
    return add_activity('photo-like', photo=photo, motdit=photo.motdit, created_by=sender)


@receiver(pre_save, sender=models.Photo)
def add_photo_activity(sender, instance=None, *args, **kwargs):
    '''Creates a "user liked photo" activity
    @TODO: what happens when we un-like a photo'''
    if not instance.id:
        return add_activity('photo-add', photo=instance, motdit=instance.motdit, created_by=instance.created_by)


@receiver(signals.opinion_approve)
def approve_opinion_activity(sender, instance=None, opinion=None, *args, **kwargs):
    '''Creates a "user approves opinion" activity'''
    return add_activity('opinion-approve', opinion=opinion, motdit=opinion.motdit, created_by=sender)
