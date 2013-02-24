import django.dispatch

poll_created = django.dispatch.Signal()
opinion_created = django.dispatch.Signal()
choice_created = django.dispatch.Signal()
voted = django.dispatch.Signal()