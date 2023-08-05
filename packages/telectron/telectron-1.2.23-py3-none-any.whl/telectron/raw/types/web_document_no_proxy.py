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


class WebDocumentNoProxy(TLObject):  # type: ignore
    """This object is a constructor of the base type :obj:`~telectron.raw.base.WebDocument`.

    Details:
        - Layer: ``129``
        - ID: ``0xf9c8bcc6``

    Parameters:
        url: ``str``
        size: ``int`` ``32-bit``
        mime_type: ``str``
        attributes: List of :obj:`DocumentAttribute <telectron.raw.base.DocumentAttribute>`
    """

    __slots__: List[str] = ["url", "size", "mime_type", "attributes"]

    ID = 0xf9c8bcc6
    QUALNAME = "types.WebDocumentNoProxy"

    def __init__(self, *, url: str, size: int, mime_type: str, attributes: List["raw.base.DocumentAttribute"]) -> None:
        self.url = url  # string
        self.size = size  # int
        self.mime_type = mime_type  # string
        self.attributes = attributes  # Vector<DocumentAttribute>

    @staticmethod
    def read(data: BytesIO, *args: Any) -> "WebDocumentNoProxy":
        # No flags
        
        url = String.read(data)
        
        size = Int.read(data)
        
        mime_type = String.read(data)
        
        attributes = TLObject.read(data)
        
        return WebDocumentNoProxy(url=url, size=size, mime_type=mime_type, attributes=attributes)

    def write(self) -> bytes:
        data = BytesIO()
        data.write(Int(self.ID, False))

        # No flags
        
        data.write(String(self.url))
        
        data.write(Int(self.size))
        
        data.write(String(self.mime_type))
        
        data.write(Vector(self.attributes))
        
        return data.getvalue()
