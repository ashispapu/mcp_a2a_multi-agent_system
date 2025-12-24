from typing import Any, List

from a2a_servers.common.agent_task_manager import AgentTaskManager
from a2a_servers.common.types import AgentCapabilities, AgentCard, AgentSkill


def generate_agent_card(
        agent_name: str,
        agent_description: str,
        agent_url: str,
        agent_version: str,
        can_stream: bool = False,
        can_push_notifications: bool = False,
        can_state_transition_history: bool = True,
        authentication: str = None,
        default_input_modes: List[str] = ["text"],
        default_output_modes: List[str] = ["text"],
        skills: List[AgentSkill] = None,
):
    """
    Generates an agent card for the Echo Agent.
    :param agent_name: The name of the agent.
    :param agent_description: The description of the agent.
    :param agent_url: The URL where the agent is hosted.
    :param agent_version: The version of the agent.
    :param can_stream: Whether the agent can stream responses.
    :param can_push_notifications: Whether the agent can send push notifications.
    :param can_state_transition_history: Whether the agent can maintain state transition history.
    :param authentication: The authentication method for the agent.
    :param default_input_modes: The default input modes for the agent.
    :param default_output_modes: The default output modes for the agent.
    :param skills: The skills of the agent.
    :return: The agent card.
    """

    return AgentCard(
        name=agent_name,
        description=agent_description,
        url=agent_url,
        version=agent_version,
        capabilities=AgentCapabilities(
            streaming=can_stream,
            pushNotifications=can_push_notifications,
            stateTransitionHistory=can_state_transition_history,
        ),
        authentication=authentication,
        defaultInputModes=default_input_modes,
        defaultOutputModes=default_output_modes,
        skills=skills,
    )


def generate_agent_task_manager(
        agent: Any,
):
    """
    Generates an agent task manager for the Echo Agent.
    :param agent: The agent instance.
    :return: The agent task manager.
    """
    return AgentTaskManager(agent)