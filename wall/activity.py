from actstream.actions import follow, unfollow
from follow.signals import created_relationship, destroyed_relationship

def handle_create_relationship(sender, user, status, **kwargs):
	if status.verb == "follow":
		follow(sender, user)
created_relationship.connect(handle_create_relationship)

def handle_destroy_relationship(sender, user, status, **kwargs):
	if status.verb == "follow":
		unfollow(sender, user)
destroyed_relationship.connect(handle_destroy_relationship)
