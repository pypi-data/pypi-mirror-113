# MIT License
# 
# Copyright (c) 2020 - Present nxtlo
# 
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
# 
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
# 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

"""Basic implementation for a Bungie a clan."""


from __future__ import annotations

__all__: Sequence[str] = ['Clan', 'ClanOwner']

from typing import (
    List,
    Sequence,
    Dict,
    Any,
    Optional,
    Union,
    TYPE_CHECKING
)

from ..utils import Image, Time
from ..error import ClanNotFound
from ..utils.enums import MembershipType

if TYPE_CHECKING:
    from datetime import datetime
    from ..types.clans import Clan as ClanPayload, ClanOwner as ClanOwnerPayload

class ClanMembers:
    __slots__: Sequence[str] = ()

class ClanOwner:
    '''Represents a Bungie clan owner.

    Attributes
    -----------
    id: `builtins.int`
        The clan owner's membership id
    name: `builtins.str`
        The clan owner's display name
    last_online: `builtins.str`
        An aware `builtins.str` version of a `datetime.datetime` object.
    type: `aiobungie.utils.enums.MembershipType`
        Returns the clan owner's membership type.
        This could be Xbox, Steam, PSN, Blizzard or ALL, if the membership type is not recognized it will return `builtins.NoneType`.
    clan_id: `builtins.int`
        The clan owner's clan id
    joined_at: Optional[datetime.datetime]:
        The clan owner's join date in UTC.
    icon: `aiobungie.utils.assets.Image`
        Returns the clan owner's icon from Image.
    is_public: `builtins.bool`
        Returns True if the clan's owner profile is public or False if not.
    types: typing.List[builtins.int]:
        returns a List of `builtins.int` of the clan owner's types.
    
    '''
    __slots__: Sequence[str] = (
        'id', 'name', 'type',
        'clan_id', 'icon', 'is_public',
        'joined_at', 'types', 'last_online'
    )
    if TYPE_CHECKING:
        id: int
        name: str
        last_online: str
        type: Optional[MembershipType]
        clan_id: int
        joined_at: str
        icon: Image
        is_public: bool
        types: List[int]

    def __init__(self, *, data: ClanOwnerPayload) -> None:
        self._update(data)

    def _update(self, data: ClanOwnerPayload) -> None:
        self.id: int = data['destinyUserInfo']['membershipId']
        self.name: str = data['destinyUserInfo']['displayName']
        self.icon: Image = Image(str(data['destinyUserInfo']['iconPath']))
        convert = int(data['lastOnlineStatusChange'])
        self.last_online: str = Time.human_timedelta(Time.from_timestamp(convert))
        self.clan_id: int = data['groupId']
        self.joined_at: str = data['joinDate']
        self.types: List[int] = data['destinyUserInfo']['applicableMembershipTypes']
        self.is_public: bool = data['destinyUserInfo']['isPublic']
        self.type: Optional[MembershipType] = MembershipType(data['destinyUserInfo'].get('membershipType', None))


    def __str__(self) -> str:
        return str(self.name)

    def __repr__(self) -> str:
        return (
            f'ClaOwner name={self.name} id={self.id} type={self.type} last_online={self.last_online}'
        )

    def __bool__(self) -> bool:
        return self.is_public

class Clan:
    """Represents a Bungie clan object.

    Attributes
    -----------
    name: `builtins.str`
        The clan's name
    id: `builtins.int`
        The clans's id
    created_at: `datetime.datetime`
        Returns the clan's creation date in UTC time.
    description: `builtins.str`
        The clan's description.
    is_public: `builtins.bool`
        Returns True if the clan is public and False if not.
    banner: `aiobungie.utils.assets.Image`
        Returns the clan's banner
    avatar: `aiobungie.utils.assets.Image`
        Returns the clan's avatar
    about: `builtins.str`
        The clan's about.
    tags: `builtins.str`
        The clan's tags
    owner: `aiobungie.objects.ClanOwner`
        Returns an object of the clan's owner.
        See `aiobungie.objects.ClanOwner` for info.
    """
    __slots__: Sequence[str] = (
        'id', 'name', 'created_at', 'edited_at',
        'member_count', 'description', 'is_public',
        'banner', 'avatar', 'about', 'tags', 'owner'
    )

    if TYPE_CHECKING:
        id: int
        name: str
        created_at: datetime
        member_count: int
        description: str
        is_public: bool
        banner: Image
        avatar: Image
        about: str
        tags: List[str]
        owner: ClanOwner

    def __init__(self, data: ClanPayload) -> None:
        self._update(data=data)

    def _update(self, data: ClanPayload) -> None:
        self.id: int = data['detail']['groupId']
        self.name: str = data['detail']['name']
        self.created_at: datetime = data['detail']['creationDate']
        self.member_count: int = data['detail']['memberCount']
        self.description: str = data['detail']['about']
        self.about: str = data['detail']['motto']
        self.is_public: bool = data['detail']['isPublic']
        self.banner: Image = Image(str(data['detail']['bannerPath']))
        self.avatar: Image = Image(str(data['detail']['avatarPath']))
        self.tags: List[str] = data['detail']['tags']
        self.owner: ClanOwner = ClanOwner(data=data['founder']) # NOTE: This works but mypy is being dumb

    def __str__(self) -> str:
        return str(self.name)


    def __repr__(self) -> Union[Any, str]:
        return (
            f'<Clan id={self.id} name={self.name} created_at={self.created_at}'
            f' owner={self.owner} is_public={self.is_public} about={self.about}'
        )