import django.dispatch

# custom signals
motdit_recommended = django.dispatch.Signal(providing_args=["motdit", ])
motdit_comment = django.dispatch.Signal(providing_args=["motdit", ])

photo_like = django.dispatch.Signal(providing_args=["motdit", ])
