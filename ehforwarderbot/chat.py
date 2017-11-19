from typing import List, Dict, Any, Optional

from .channel import EFBChannel
from .constants import ChatType


class EFBChat:
    """
    EFB Chat object. This is used to represent a chat or a group member.

    Attributes:
        channel_id (str): Unique ID of the channel.
        channel_emoji (str): Emoji of the channel.
        channel_name (str): Name of the channel.
        chat_name (str): Name of the chat.
        chat_alias (str): Alternative name of the chat, usually set by user.
        chat_type (:obj:`ehforwarderbot.ChatType`): Type of the chat.
        chat_uid (str): Unique ID of the chat. This should be unique within the channel.
        is_chat (bool): Indicate if this object represents a chat. Defaulted to ``True``.
            This should be set to ``False`` when used on a group member.
        group (:obj:`ehforwarderbot.EFBChat` or None): The parent chat of the member. Only
            available to chat member objects. Defaulted to ``None``.
        members (list of :obj:`ehforwarderbot.EFBChat`): Provide a list of members
            in the group. Defaulted to an empty ``list``. You may want to extend this
            object and implement a ``@property`` method set for loading chats on
            demand.
        vendor_specific (Dict[str, Any]): Any vendor specific attributes.
    """

    def __init__(self, channel=None):
        """
        Args:
            channel (:obj:`ehforwarderbot.EFBChannel`, optional):
                Provide the channel object to fill ``channel_name``,
                ``channel_emoji``, and ``channel_id`` automatically.
        """
        if isinstance(channel, EFBChannel):
            self.channel_name: str = channel.channel_name
            self.channel_emoji: str = channel.channel_emoji
            self.channel_id: str = channel.channel_id

        self.chat_name: str = None
        self.chat_type: ChatType = None
        self.chat_alias: str = None
        self.chat_uid: str = None
        self.is_chat: bool = True
        self.members: List[EFBChat] = []
        self.group: Optional[EFBChat] = None
        self.vendor_specific: Dict[str, Any] = dict()

    def self(self) -> 'EFBChat':
        """
        Set the chat as yourself.
        In this context, "yourself" means the user behind the master channel.
        Every channel should relate this to the corresponding target.

        Returns:
            EFBChat: This object.
        """
        self.chat_name = "You"
        self.chat_alias = None
        self.chat_uid = "__self__"
        self.chat_type = ChatType.User
        return self

    def system(self) -> 'EFBChat':
        """
        Set the chat as a system chat.
        Only set for channel-level and group-level system chats.

        Returns:
            EFBChat: This object.
        """
        self.chat_name = "System"
        self.chat_alias = None
        self.chat_uid = "__system__"
        self.chat_type = ChatType.User
        return self

    @property
    def is_self(self) -> bool:
        return self.chat_uid == "__self__"

    @property
    def is_system(self) -> bool:
        return self.chat_uid == "__system__"

    def __eq__(self, other):
        return self.channel_id == other.channel_id and self.chat_uid == other.chat_uid

    # TODO: Add __str__
