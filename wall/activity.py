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
	action.send(sender.author, verb=" has created a poll ",action_object=sender)
poll_created.connect(handle_poll_created)

def handle_opinion_created(sender, **kwargs):
	action.send(sender.author, verb=" wote an Opinion ",action_object=sender)
opinion_created.connect(handle_opinion_created)

def handle_choice_created(sender, **kwargs):
	action.send(sender.author, verb=" added a choice to a poll ",action_object=sender)
choice_created.connect(handle_choice_created)

def handle_vote_created(sender, **kwargs):
	action.send(sender.author, verb=" voted on a poll ",action_object=sender)
voted.connect(handle_vote_created)

