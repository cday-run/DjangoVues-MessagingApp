from django.shortcuts import render

from django.contrib.auth import get_user_model

from rest_framework import permissions
from rest_framework.views import APIView
from rest_framework.response import Response

from .models import (ChatSession, ChatSessionMessage, ChatSessionPerson, deserialize_user)


#Create a class based view to handle the creating and adding users to a chat session
class ChatSessionView(APIView):
	permission_classes = (permissions.IsAuthenticated,)

	def post(self, request, *ards, **kwargs):
		user = request.user
		chat_session = ChatSession.objects.create(owner=user)

		return Response({
			'status': 200,
			'uri': chat_session.uri,
			'message': 'New session successfully created!'
		})

	def patch(self, request, *args, **kwargs):
		#Get the user and chat session information
		User = get_user_model()
		uri = kwargs['uri']
		username = request.data['username']
		user = User.objects.get(username=username)
		chat_session = ChatSession.objects.get(uri=uri)
		owner = chat_session.owner

		#only allow users who aren't owner to join the session
		if owner != user:
			chat_session.people.get_or_create(user=user, chat_session=chat_session)

		owner = deserialize_user(owner)
		people = [
			deserialize_user(chat_session.user)
			for chat_session in chat_session.people.all()
		]

		#make owner of session the first person in session
		people.insert(0, owner)

		return Response ({
			'status': 200,
			'people': people,
			'message': '%s joined the session' %user.username,
			'user': deserialize_user(user)
		})

#Create a class based view to handle adding messages to the Chat
class ChatMessageView(APIView):
	permission_classes = (permissions.IsAuthenticated,)

	'''Get the messages of the chat room'''
	def get(self, request, *args, **kwargs):
		#fetch chat room uri
		uri = kwargs['uri']

		#get the appropriate chat room
		chat_session = ChatSession.objects.get(uri=uri)

		'''find more efficient way to do this - look at twitter app'''
		#retrieve all the messages in the chat room
		messages = [
			chat_session_message.to_json()
			for chat_session_message in chat_session_messages.all()
		]

		return Response ({
			'id': chat_session.id,
			'uri': chat_session.uri,
			'messages': messages
		})

	'''have a method to create messages in the chat room'''
	def post(self, request, *args, **kwargs):
		uri = kwargs['uri']
		user = request.user
		chat_session = ChatSession.objects.get(uri=uri)
		message = request.data['message']

		#Create the message in the database
		ChatSessionMessage.objects.create(
			user=user,
			chat_session=chat_session,
			message=message
		)

		return Response ({
			'status': 200,
			'uri': chat_session.uri,
			'user': deserialize_user(user),
			'message': message,
		})