from rest_framework import serializers

from chatsapp.models import Chat, Contact, Message
from chatsapp.views import get_user_contact




class ContactSerializer(serializers.StringRelatedField):
    def to_internal_value(self, value):
        return value

class MessageSerializer(serializers.ModelSerializer):

    class Meta:
        model = Message
        fields = ('__all__')


class ChatSerializer(serializers.ModelSerializer):
    participants = ContactSerializer(many=True)
    messages = MessageSerializer(many=True)

    class Meta:
        model = Chat
        fields = ('id', 'messages', 'participants', 'owner', 'name')
        read_only = ('id')

    def create(self, validated_data):
        print(validated_data)
        participants = validated_data.pop('participants')
        chat = Chat()
        chat.save()
        for username in participants:
            contact = get_user_contact(username)
            chat.participants.add(contact)
        chat.save()
        return chat



# do in python shell to see how to serialize data

# from chat.models import Chat
# from chat.api.serializers import ChatSerializer
# chat = Chat.objects.get(id=1)
# s = ChatSerializer(instance=chat)
# s
# s.data
