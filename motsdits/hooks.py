from django.db.models.signals import pre_save
from django.dispatch import receiver
from motsdits.models import User
from django.core.exceptions import ValidationError


def ensure_http(url):
    '''Ensures a URL starts with the protocol string'''
    if not url.startswith('http'):
        url = 'http://{url}'.format(url=url)
    return url


@receiver(pre_save, sender=User)
def format_twitter(sender, instance, *args, **kwargs):
    '''Formats a user twitter handle as a URL'''
    if instance.twitter:

        # Check for @user
        if instance.twitter.startswith('@'):
            instance.twitter = 'twitter.com/{handle}'.format(handle=instance.twitter[1:])
        elif not 'twitter' in instance.twitter and '/' in instance.twitter:
            raise ValidationError("Twitter handles must either be a username or a full url")

        instance.twitter = ensure_http(instance.twitter)


@receiver(pre_save, sender=User)
def format_facebook(sender, instance, *args, **kwargs):
    '''Ensures the facebook url is in the right format'''
    if instance.facebook:
        instance.facebook = ensure_http(instance.facebook)


@receiver(pre_save, sender=User)
def format_website(sender, instance, *args, **kwargs):
    '''Ensures the website url is in the right format'''
    if instance.website:
        instance.website = ensure_http(instance.website)
