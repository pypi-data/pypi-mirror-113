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


class SendMessage(TLObject):  # type: ignore
    """Telegram API method.

    Details:
        - Layer: ``129``
        - ID: ``0x520c3870``

    Parameters:
        peer: :obj:`InputPeer <telectron.raw.base.InputPeer>`
        message: ``str``
        random_id: ``int`` ``64-bit``
        no_webpage (optional): ``bool``
        silent (optional): ``bool``
        background (optional): ``bool``
        clear_draft (optional): ``bool``
        reply_to_msg_id (optional): ``int`` ``32-bit``
        reply_markup (optional): :obj:`ReplyMarkup <telectron.raw.base.ReplyMarkup>`
        entities (optional): List of :obj:`MessageEntity <telectron.raw.base.MessageEntity>`
        schedule_date (optional): ``int`` ``32-bit``

    Returns:
        :obj:`Updates <telectron.raw.base.Updates>`
    """

    __slots__: List[str] = ["peer", "message", "random_id", "no_webpage", "silent", "background", "clear_draft", "reply_to_msg_id", "reply_markup", "entities", "schedule_date"]

    ID = 0x520c3870
    QUALNAME = "functions.messages.SendMessage"

    def __init__(self, *, peer: "raw.base.InputPeer", message: str, random_id: int, no_webpage: Union[None, bool] = None, silent: Union[None, bool] = None, background: Union[None, bool] = None, clear_draft: Union[None, bool] = None, reply_to_msg_id: Union[None, int] = None, reply_markup: "raw.base.ReplyMarkup" = None, entities: Union[None, List["raw.base.MessageEntity"]] = None, schedule_date: Union[None, int] = None) -> None:
        self.peer = peer  # InputPeer
        self.message = message  # string
        self.random_id = random_id  # long
        self.no_webpage = no_webpage  # flags.1?true
        self.silent = silent  # flags.5?true
        self.background = background  # flags.6?true
        self.clear_draft = clear_draft  # flags.7?true
        self.reply_to_msg_id = reply_to_msg_id  # flags.0?int
        self.reply_markup = reply_markup  # flags.2?ReplyMarkup
        self.entities = entities  # flags.3?Vector<MessageEntity>
        self.schedule_date = schedule_date  # flags.10?int

    @staticmethod
    def read(data: BytesIO, *args: Any) -> "SendMessage":
        flags = Int.read(data)
        
        no_webpage = True if flags & (1 << 1) else False
        silent = True if flags & (1 << 5) else False
        background = True if flags & (1 << 6) else False
        clear_draft = True if flags & (1 << 7) else False
        peer = TLObject.read(data)
        
        reply_to_msg_id = Int.read(data) if flags & (1 << 0) else None
        message = String.read(data)
        
        random_id = Long.read(data)
        
        reply_markup = TLObject.read(data) if flags & (1 << 2) else None
        
        entities = TLObject.read(data) if flags & (1 << 3) else []
        
        schedule_date = Int.read(data) if flags & (1 << 10) else None
        return SendMessage(peer=peer, message=message, random_id=random_id, no_webpage=no_webpage, silent=silent, background=background, clear_draft=clear_draft, reply_to_msg_id=reply_to_msg_id, reply_markup=reply_markup, entities=entities, schedule_date=schedule_date)

    def write(self) -> bytes:
        data = BytesIO()
        data.write(Int(self.ID, False))

        flags = 0
        flags |= (1 << 1) if self.no_webpage else 0
        flags |= (1 << 5) if self.silent else 0
        flags |= (1 << 6) if self.background else 0
        flags |= (1 << 7) if self.clear_draft else 0
        flags |= (1 << 0) if self.reply_to_msg_id is not None else 0
        flags |= (1 << 2) if self.reply_markup is not None else 0
        flags |= (1 << 3) if self.entities is not None else 0
        flags |= (1 << 10) if self.schedule_date is not None else 0
        data.write(Int(flags))
        
        data.write(self.peer.write())
        
        if self.reply_to_msg_id is not None:
            data.write(Int(self.reply_to_msg_id))
        
        data.write(String(self.message))
        
        data.write(Long(self.random_id))
        
        if self.reply_markup is not None:
            data.write(self.reply_markup.write())
        
        if self.entities is not None:
            data.write(Vector(self.entities))
        
        if self.schedule_date is not None:
            data.write(Int(self.schedule_date))
        
        return data.getvalue()
