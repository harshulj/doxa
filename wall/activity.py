from actstream import actions
from actstream import action
from follow.signals import created_relationship, destroyed_relationship
from polls_and_opinions.signals import poll_created, opinion_created, choice_created, voted
from polls_and_opinions.models import Poll, Opinion, Vote, Choice

def handle_create_relationship(sender, user, status, **kwargs):
	if status.verb == "follow":
		actions.follow(sender, user)
created_relationship.connect(handle_create_relationship)

def handle_destroy_relationship(sender, user, status, **kwargs):
	if status.verb == "follow":
		actions.unfollow(sender, user)
destroyed_relationship.connect(handle_destroy_relationship)

def handle_poll_created(sender, **kwargs):
	for user in sender.author.relationships.followers():
		action.send(sender.author, verb=" has created a poll ",action_object=sender)
poll_created.connect(handle_poll_created)

