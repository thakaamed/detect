from agent.api.views import *
from django.urls import path



urlpatterns = [
    path("get-or-create-agent-keys", get_or_create_agent_keys, name="getOrCreateAgentKeys"),
]