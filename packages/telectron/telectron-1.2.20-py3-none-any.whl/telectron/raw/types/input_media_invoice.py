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


class InputMediaInvoice(TLObject):  # type: ignore
    """This object is a constructor of the base type :obj:`~telectron.raw.base.InputMedia`.

    Details:
        - Layer: ``129``
        - ID: ``0xd9799874``

    Parameters:
        title: ``str``
        description: ``str``
        invoice: :obj:`Invoice <telectron.raw.base.Invoice>`
        payload: ``bytes``
        provider: ``str``
        provider_data: :obj:`DataJSON <telectron.raw.base.DataJSON>`
        photo (optional): :obj:`InputWebDocument <telectron.raw.base.InputWebDocument>`
        start_param (optional): ``str``
    """

    __slots__: List[str] = ["title", "description", "invoice", "payload", "provider", "provider_data", "photo", "start_param"]

    ID = 0xd9799874
    QUALNAME = "types.InputMediaInvoice"

    def __init__(self, *, title: str, description: str, invoice: "raw.base.Invoice", payload: bytes, provider: str, provider_data: "raw.base.DataJSON", photo: "raw.base.InputWebDocument" = None, start_param: Union[None, str] = None) -> None:
        self.title = title  # string
        self.description = description  # string
        self.invoice = invoice  # Invoice
        self.payload = payload  # bytes
        self.provider = provider  # string
        self.provider_data = provider_data  # DataJSON
        self.photo = photo  # flags.0?InputWebDocument
        self.start_param = start_param  # flags.1?string

    @staticmethod
    def read(data: BytesIO, *args: Any) -> "InputMediaInvoice":
        flags = Int.read(data)
        
        title = String.read(data)
        
        description = String.read(data)
        
        photo = TLObject.read(data) if flags & (1 << 0) else None
        
        invoice = TLObject.read(data)
        
        payload = Bytes.read(data)
        
        provider = String.read(data)
        
        provider_data = TLObject.read(data)
        
        start_param = String.read(data) if flags & (1 << 1) else None
        return InputMediaInvoice(title=title, description=description, invoice=invoice, payload=payload, provider=provider, provider_data=provider_data, photo=photo, start_param=start_param)

    def write(self) -> bytes:
        data = BytesIO()
        data.write(Int(self.ID, False))

        flags = 0
        flags |= (1 << 0) if self.photo is not None else 0
        flags |= (1 << 1) if self.start_param is not None else 0
        data.write(Int(flags))
        
        data.write(String(self.title))
        
        data.write(String(self.description))
        
        if self.photo is not None:
            data.write(self.photo.write())
        
        data.write(self.invoice.write())
        
        data.write(Bytes(self.payload))
        
        data.write(String(self.provider))
        
        data.write(self.provider_data.write())
        
        if self.start_param is not None:
            data.write(String(self.start_param))
        
        return data.getvalue()
