from django.dispatch import Signal

created_relationship = Signal(providing_args=["user", "status"])
destroyed_relationship = Signal(providing_args=["user", "status"])
