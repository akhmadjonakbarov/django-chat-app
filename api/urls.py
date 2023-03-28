from django.urls import path
from .views import (ApiInfoView,ChatListView, ChatDetailView,
                    ChatDeleteView, ChatCreateView, ChatUpdateView,)
urlpatterns = [
    path('',ApiInfoView.as_view()),
    path('read/', ChatListView.as_view()),
    path('create/', ChatCreateView.as_view()),
    path('detail/<int:id>/', ChatDetailView.as_view()),
    path('update/pk/', ChatUpdateView.as_view()),
    path('delete/<int:id>/', ChatDeleteView.as_view())
]
