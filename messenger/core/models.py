from django.db import models
from django.contrib.auth import get_user_model
from uuid import uuid4

User = get_user_model()

#Deserialize use instance to JSON
def deserialize_user(user):
	return {
		'id': user.id,
		'username': user.username,
		'email': user.email,
	}

#Creat URI for chat session
def _generate_uri():
	return str(uuid4()).replace('-', '')[:15]

#Model to track creation/update date for a model
class ChangeDateModel(models.Model):
	create_date = models.DateTimeField(auto_now_add=True)
	update_date = models.DateTimeField(auto_now=True)

	class Meta:
		abstract=True

#Create model that represents a given chat session
class ChatSession(ChangeDateModel):
	owner = models.ForeignKey(User, on_delete=models.PROTECT)
	uri = models.URLField(default=_generate_uri)

#Create model that represents and stores messages from a session
class ChatSessionMessage(ChangeDateModel):
	user = models.ForeignKey(User, on_delete=models.PROTECT)
	chat_session = models.ForeignKey(ChatSession, related_name='messages', on_delete=models.PROTECT)
	message = models.TextField(max_length=1000)

	def to_json(self):
		return {'user': deserialize_user(self.user), 'message': self.message}

#Create a model that represnts and stores users from a session
class ChatSessionPerson(ChangeDateModel):
	chat_session = models.ForeignKey(ChatSession, related_name='people', on_delete=models.PROTECT)
	user = models.ForeignKey(User, on_delete=models.PROTECT)