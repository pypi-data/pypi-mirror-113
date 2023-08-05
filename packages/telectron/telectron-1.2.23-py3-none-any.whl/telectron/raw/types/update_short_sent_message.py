#  telectron - Telegram MTProto API Client Library for Python
#  Copyright (C) 2017-2021 Dan <https://github.com/delivrance>
#
#  This file is part of telectron.
#
#  telectron is free software: you can redistribute it and/or modify
#  it under the terms of the GNU Lesser General Public License as published
#  by the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  telectron is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU Lesser General Public License for more details.
#
#  You should have received a copy of the GNU Lesser General Public License
#  along with telectron.  If not, see <http://www.gnu.org/licenses/>.

from io import BytesIO

from telectron.raw.core.primitives import Int, Long, Int128, Int256, Bool, Bytes, String, Double, Vector
from telectron.raw.core import TLObject
from telectron import raw
from typing import List, Union, Any

# # # # # # # # # # # # # # # # # # # # # # # #
#               !!! WARNING !!!               #
#          This is a generated file!          #
# All changes made in this file will be lost! #
# # # # # # # # # # # # # # # # # # # # # # # #


class UpdateShortSentMessage(TLObject):  # type: ignore
    """This object is a constructor of the base type :obj:`~telectron.raw.base.Updates`.

    Details:
        - Layer: ``129``
        - ID: ``0x9015e101``

    Parameters:
        id: ``int`` ``32-bit``
        pts: ``int`` ``32-bit``
        pts_count: ``int`` ``32-bit``
        date: ``int`` ``32-bit``
        out (optional): ``bool``
        media (optional): :obj:`MessageMedia <telectron.raw.base.MessageMedia>`
        entities (optional): List of :obj:`MessageEntity <telectron.raw.base.MessageEntity>`
        ttl_period (optional): ``int`` ``32-bit``

    See Also:
        This object can be returned by 62 methods:

        .. hlist::
            :columns: 2

            - :obj:`account.GetNotifyExceptions <telectron.raw.functions.account.GetNotifyExceptions>`
            - :obj:`contacts.DeleteContacts <telectron.raw.functions.contacts.DeleteContacts>`
            - :obj:`contacts.AddContact <telectron.raw.functions.contacts.AddContact>`
            - :obj:`contacts.AcceptContact <telectron.raw.functions.contacts.AcceptContact>`
            - :obj:`contacts.GetLocated <telectron.raw.functions.contacts.GetLocated>`
            - :obj:`contacts.BlockFromReplies <telectron.raw.functions.contacts.BlockFromReplies>`
            - :obj:`messages.SendMessage <telectron.raw.functions.messages.SendMessage>`
            - :obj:`messages.SendMedia <telectron.raw.functions.messages.SendMedia>`
            - :obj:`messages.ForwardMessages <telectron.raw.functions.messages.ForwardMessages>`
            - :obj:`messages.EditChatTitle <telectron.raw.functions.messages.EditChatTitle>`
            - :obj:`messages.EditChatPhoto <telectron.raw.functions.messages.EditChatPhoto>`
            - :obj:`messages.AddChatUser <telectron.raw.functions.messages.AddChatUser>`
            - :obj:`messages.DeleteChatUser <telectron.raw.functions.messages.DeleteChatUser>`
            - :obj:`messages.CreateChat <telectron.raw.functions.messages.CreateChat>`
            - :obj:`messages.ImportChatInvite <telectron.raw.functions.messages.ImportChatInvite>`
            - :obj:`messages.StartBot <telectron.raw.functions.messages.StartBot>`
            - :obj:`messages.MigrateChat <telectron.raw.functions.messages.MigrateChat>`
            - :obj:`messages.SendInlineBotResult <telectron.raw.functions.messages.SendInlineBotResult>`
            - :obj:`messages.EditMessage <telectron.raw.functions.messages.EditMessage>`
            - :obj:`messages.GetAllDrafts <telectron.raw.functions.messages.GetAllDrafts>`
            - :obj:`messages.SetGameScore <telectron.raw.functions.messages.SetGameScore>`
            - :obj:`messages.SendScreenshotNotification <telectron.raw.functions.messages.SendScreenshotNotification>`
            - :obj:`messages.SendMultiMedia <telectron.raw.functions.messages.SendMultiMedia>`
            - :obj:`messages.UpdatePinnedMessage <telectron.raw.functions.messages.UpdatePinnedMessage>`
            - :obj:`messages.SendVote <telectron.raw.functions.messages.SendVote>`
            - :obj:`messages.GetPollResults <telectron.raw.functions.messages.GetPollResults>`
            - :obj:`messages.EditChatDefaultBannedRights <telectron.raw.functions.messages.EditChatDefaultBannedRights>`
            - :obj:`messages.SendScheduledMessages <telectron.raw.functions.messages.SendScheduledMessages>`
            - :obj:`messages.DeleteScheduledMessages <telectron.raw.functions.messages.DeleteScheduledMessages>`
            - :obj:`messages.SetHistoryTTL <telectron.raw.functions.messages.SetHistoryTTL>`
            - :obj:`help.GetAppChangelog <telectron.raw.functions.help.GetAppChangelog>`
            - :obj:`channels.CreateChannel <telectron.raw.functions.channels.CreateChannel>`
            - :obj:`channels.EditAdmin <telectron.raw.functions.channels.EditAdmin>`
            - :obj:`channels.EditTitle <telectron.raw.functions.channels.EditTitle>`
            - :obj:`channels.EditPhoto <telectron.raw.functions.channels.EditPhoto>`
            - :obj:`channels.JoinChannel <telectron.raw.functions.channels.JoinChannel>`
            - :obj:`channels.LeaveChannel <telectron.raw.functions.channels.LeaveChannel>`
            - :obj:`channels.InviteToChannel <telectron.raw.functions.channels.InviteToChannel>`
            - :obj:`channels.DeleteChannel <telectron.raw.functions.channels.DeleteChannel>`
            - :obj:`channels.ToggleSignatures <telectron.raw.functions.channels.ToggleSignatures>`
            - :obj:`channels.EditBanned <telectron.raw.functions.channels.EditBanned>`
            - :obj:`channels.TogglePreHistoryHidden <telectron.raw.functions.channels.TogglePreHistoryHidden>`
            - :obj:`channels.EditCreator <telectron.raw.functions.channels.EditCreator>`
            - :obj:`channels.ToggleSlowMode <telectron.raw.functions.channels.ToggleSlowMode>`
            - :obj:`channels.ConvertToGigagroup <telectron.raw.functions.channels.ConvertToGigagroup>`
            - :obj:`phone.DiscardCall <telectron.raw.functions.phone.DiscardCall>`
            - :obj:`phone.SetCallRating <telectron.raw.functions.phone.SetCallRating>`
            - :obj:`phone.CreateGroupCall <telectron.raw.functions.phone.CreateGroupCall>`
            - :obj:`phone.JoinGroupCall <telectron.raw.functions.phone.JoinGroupCall>`
            - :obj:`phone.LeaveGroupCall <telectron.raw.functions.phone.LeaveGroupCall>`
            - :obj:`phone.InviteToGroupCall <telectron.raw.functions.phone.InviteToGroupCall>`
            - :obj:`phone.DiscardGroupCall <telectron.raw.functions.phone.DiscardGroupCall>`
            - :obj:`phone.ToggleGroupCallSettings <telectron.raw.functions.phone.ToggleGroupCallSettings>`
            - :obj:`phone.ToggleGroupCallRecord <telectron.raw.functions.phone.ToggleGroupCallRecord>`
            - :obj:`phone.EditGroupCallParticipant <telectron.raw.functions.phone.EditGroupCallParticipant>`
            - :obj:`phone.EditGroupCallTitle <telectron.raw.functions.phone.EditGroupCallTitle>`
            - :obj:`phone.ToggleGroupCallStartSubscription <telectron.raw.functions.phone.ToggleGroupCallStartSubscription>`
            - :obj:`phone.StartScheduledGroupCall <telectron.raw.functions.phone.StartScheduledGroupCall>`
            - :obj:`phone.JoinGroupCallPresentation <telectron.raw.functions.phone.JoinGroupCallPresentation>`
            - :obj:`phone.LeaveGroupCallPresentation <telectron.raw.functions.phone.LeaveGroupCallPresentation>`
            - :obj:`folders.EditPeerFolders <telectron.raw.functions.folders.EditPeerFolders>`
            - :obj:`folders.DeleteFolder <telectron.raw.functions.folders.DeleteFolder>`
    """

    __slots__: List[str] = ["id", "pts", "pts_count", "date", "out", "media", "entities", "ttl_period"]

    ID = 0x9015e101
    QUALNAME = "types.UpdateShortSentMessage"

    def __init__(self, *, id: int, pts: int, pts_count: int, date: int, out: Union[None, bool] = None, media: "raw.base.MessageMedia" = None, entities: Union[None, List["raw.base.MessageEntity"]] = None, ttl_period: Union[None, int] = None) -> None:
        self.id = id  # int
        self.pts = pts  # int
        self.pts_count = pts_count  # int
        self.date = date  # int
        self.out = out  # flags.1?true
        self.media = media  # flags.9?MessageMedia
        self.entities = entities  # flags.7?Vector<MessageEntity>
        self.ttl_period = ttl_period  # flags.25?int

    @staticmethod
    def read(data: BytesIO, *args: Any) -> "UpdateShortSentMessage":
        flags = Int.read(data)
        
        out = True if flags & (1 << 1) else False
        id = Int.read(data)
        
        pts = Int.read(data)
        
        pts_count = Int.read(data)
        
        date = Int.read(data)
        
        media = TLObject.read(data) if flags & (1 << 9) else None
        
        entities = TLObject.read(data) if flags & (1 << 7) else []
        
        ttl_period = Int.read(data) if flags & (1 << 25) else None
        return UpdateShortSentMessage(id=id, pts=pts, pts_count=pts_count, date=date, out=out, media=media, entities=entities, ttl_period=ttl_period)

    def write(self) -> bytes:
        data = BytesIO()
        data.write(Int(self.ID, False))

        flags = 0
        flags |= (1 << 1) if self.out else 0
        flags |= (1 << 9) if self.media is not None else 0
        flags |= (1 << 7) if self.entities is not None else 0
        flags |= (1 << 25) if self.ttl_period is not None else 0
        data.write(Int(flags))
        
        data.write(Int(self.id))
        
        data.write(Int(self.pts))
        
        data.write(Int(self.pts_count))
        
        data.write(Int(self.date))
        
        if self.media is not None:
            data.write(self.media.write())
        
        if self.entities is not None:
            data.write(Vector(self.entities))
        
        if self.ttl_period is not None:
            data.write(Int(self.ttl_period))
        
        return data.getvalue()
