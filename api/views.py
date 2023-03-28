from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from rest_framework.generics import GenericAPIView
from rest_framework.views import APIView
from rest_framework.response import Response

from rest_framework.permissions import (AllowAny, IsAdminUser)
from chatsapp.models import (Contact, Chat, Message)
from .serializers import ChatSerializer

User = get_user_model()


def get_user_contact(username: str):
    user = get_object_or_404(User, username=username)
    contact = get_object_or_404(Contact, user=user)
    return contact

class ApiInfoView(APIView):
    permission_classes = (AllowAny, )
    def get(self, request):
        routes = [
            {"GET":"api/read/"},
            {"GET":"api/create/"}, 
            {"GET":"api/detail/id/"},
            {"GET":"api/update/id/"},
            {"GET":"api/delete/id/"}
        ]
        return Response(routes)



class ChatListView(GenericAPIView):
    serializer_class = ChatSerializer
    permission_classes = (AllowAny,)
    queryset = Chat.objects.all()

    def get(self, request):
        chats = self.queryset.all()
        username = self.request.query_params.get('username', None)
        serializer = self.get_serializer(chats, many=True)
        if username is not None:
            contact = get_user_contact(username=username)
            chats = contact.chats.all()
        return Response(serializer.data)


class ChatCreateView(GenericAPIView):
    permission_classes = (AllowAny,)
    queryset = Chat.objects.all()
    serializer_class = ChatSerializer

    # def get(self, request):
    #     return Response()

    def post(self, request):
        group_name = request.data['name']
        # ownerId = request.data['owner']
        # owner = User.objects.get(id=owner/Id)
        chat = Chat.objects.create(name=group_name, owner=request.user)
        serializer = self.get_serializer(chat,many=False)
        return Response(serializer.data)



class ChatDetailView(GenericAPIView):
    permission_classes = (AllowAny,)
    queryset = Chat.objects.all()
    serializer_class = ChatSerializer
    def get(self, request, id):
        chat = self.queryset.get(id=id)
        serializer = self.get_serializer(chat,many=False)
        return Response(serializer.data)


class ChatUpdateView(GenericAPIView):
    serializer_class = ChatSerializer
    permission_classes = (AllowAny,)
    queryset = Chat.objects.all()


class ChatDeleteView(GenericAPIView):
    serializer_class = ChatSerializer
    permission_classes = (AllowAny,)
    queryset = Chat.objects.all()

    def delete(self, request, id):
        print(id)
        chat = self.queryset.get(id=id)
        if chat is not None:
            chat.delete()
        return Response({"data":"success"})
