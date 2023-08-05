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


class BotInlineMessageText(TLObject):  # type: ignore
    """This object is a constructor of the base type :obj:`~telectron.raw.base.BotInlineMessage`.

    Details:
        - Layer: ``129``
        - ID: ``0x8c7f65e2``

    Parameters:
        message: ``str``
        no_webpage (optional): ``bool``
        entities (optional): List of :obj:`MessageEntity <telectron.raw.base.MessageEntity>`
        reply_markup (optional): :obj:`ReplyMarkup <telectron.raw.base.ReplyMarkup>`
    """

    __slots__: List[str] = ["message", "no_webpage", "entities", "reply_markup"]

    ID = 0x8c7f65e2
    QUALNAME = "types.BotInlineMessageText"

    def __init__(self, *, message: str, no_webpage: Union[None, bool] = None, entities: Union[None, List["raw.base.MessageEntity"]] = None, reply_markup: "raw.base.ReplyMarkup" = None) -> None:
        self.message = message  # string
        self.no_webpage = no_webpage  # flags.0?true
        self.entities = entities  # flags.1?Vector<MessageEntity>
        self.reply_markup = reply_markup  # flags.2?ReplyMarkup

    @staticmethod
    def read(data: BytesIO, *args: Any) -> "BotInlineMessageText":
        flags = Int.read(data)
        
        no_webpage = True if flags & (1 << 0) else False
        message = String.read(data)
        
        entities = TLObject.read(data) if flags & (1 << 1) else []
        
        reply_markup = TLObject.read(data) if flags & (1 << 2) else None
        
        return BotInlineMessageText(message=message, no_webpage=no_webpage, entities=entities, reply_markup=reply_markup)

    def write(self) -> bytes:
        data = BytesIO()
        data.write(Int(self.ID, False))

        flags = 0
        flags |= (1 << 0) if self.no_webpage else 0
        flags |= (1 << 1) if self.entities is not None else 0
        flags |= (1 << 2) if self.reply_markup is not None else 0
        data.write(Int(flags))
        
        data.write(String(self.message))
        
        if self.entities is not None:
            data.write(Vector(self.entities))
        
        if self.reply_markup is not None:
            data.write(self.reply_markup.write())
        
        return data.getvalue()
