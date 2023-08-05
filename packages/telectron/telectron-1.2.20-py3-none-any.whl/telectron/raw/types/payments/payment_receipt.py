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


class PaymentReceipt(TLObject):  # type: ignore
    """This object is a constructor of the base type :obj:`~telectron.raw.base.payments.PaymentReceipt`.

    Details:
        - Layer: ``129``
        - ID: ``0x10b555d0``

    Parameters:
        date: ``int`` ``32-bit``
        bot_id: ``int`` ``32-bit``
        provider_id: ``int`` ``32-bit``
        title: ``str``
        description: ``str``
        invoice: :obj:`Invoice <telectron.raw.base.Invoice>`
        currency: ``str``
        total_amount: ``int`` ``64-bit``
        credentials_title: ``str``
        users: List of :obj:`User <telectron.raw.base.User>`
        photo (optional): :obj:`WebDocument <telectron.raw.base.WebDocument>`
        info (optional): :obj:`PaymentRequestedInfo <telectron.raw.base.PaymentRequestedInfo>`
        shipping (optional): :obj:`ShippingOption <telectron.raw.base.ShippingOption>`
        tip_amount (optional): ``int`` ``64-bit``

    See Also:
        This object can be returned by 1 method:

        .. hlist::
            :columns: 2

            - :obj:`payments.GetPaymentReceipt <telectron.raw.functions.payments.GetPaymentReceipt>`
    """

    __slots__: List[str] = ["date", "bot_id", "provider_id", "title", "description", "invoice", "currency", "total_amount", "credentials_title", "users", "photo", "info", "shipping", "tip_amount"]

    ID = 0x10b555d0
    QUALNAME = "types.payments.PaymentReceipt"

    def __init__(self, *, date: int, bot_id: int, provider_id: int, title: str, description: str, invoice: "raw.base.Invoice", currency: str, total_amount: int, credentials_title: str, users: List["raw.base.User"], photo: "raw.base.WebDocument" = None, info: "raw.base.PaymentRequestedInfo" = None, shipping: "raw.base.ShippingOption" = None, tip_amount: Union[None, int] = None) -> None:
        self.date = date  # int
        self.bot_id = bot_id  # int
        self.provider_id = provider_id  # int
        self.title = title  # string
        self.description = description  # string
        self.invoice = invoice  # Invoice
        self.currency = currency  # string
        self.total_amount = total_amount  # long
        self.credentials_title = credentials_title  # string
        self.users = users  # Vector<User>
        self.photo = photo  # flags.2?WebDocument
        self.info = info  # flags.0?PaymentRequestedInfo
        self.shipping = shipping  # flags.1?ShippingOption
        self.tip_amount = tip_amount  # flags.3?long

    @staticmethod
    def read(data: BytesIO, *args: Any) -> "PaymentReceipt":
        flags = Int.read(data)
        
        date = Int.read(data)
        
        bot_id = Int.read(data)
        
        provider_id = Int.read(data)
        
        title = String.read(data)
        
        description = String.read(data)
        
        photo = TLObject.read(data) if flags & (1 << 2) else None
        
        invoice = TLObject.read(data)
        
        info = TLObject.read(data) if flags & (1 << 0) else None
        
        shipping = TLObject.read(data) if flags & (1 << 1) else None
        
        tip_amount = Long.read(data) if flags & (1 << 3) else None
        currency = String.read(data)
        
        total_amount = Long.read(data)
        
        credentials_title = String.read(data)
        
        users = TLObject.read(data)
        
        return PaymentReceipt(date=date, bot_id=bot_id, provider_id=provider_id, title=title, description=description, invoice=invoice, currency=currency, total_amount=total_amount, credentials_title=credentials_title, users=users, photo=photo, info=info, shipping=shipping, tip_amount=tip_amount)

    def write(self) -> bytes:
        data = BytesIO()
        data.write(Int(self.ID, False))

        flags = 0
        flags |= (1 << 2) if self.photo is not None else 0
        flags |= (1 << 0) if self.info is not None else 0
        flags |= (1 << 1) if self.shipping is not None else 0
        flags |= (1 << 3) if self.tip_amount is not None else 0
        data.write(Int(flags))
        
        data.write(Int(self.date))
        
        data.write(Int(self.bot_id))
        
        data.write(Int(self.provider_id))
        
        data.write(String(self.title))
        
        data.write(String(self.description))
        
        if self.photo is not None:
            data.write(self.photo.write())
        
        data.write(self.invoice.write())
        
        if self.info is not None:
            data.write(self.info.write())
        
        if self.shipping is not None:
            data.write(self.shipping.write())
        
        if self.tip_amount is not None:
            data.write(Long(self.tip_amount))
        
        data.write(String(self.currency))
        
        data.write(Long(self.total_amount))
        
        data.write(String(self.credentials_title))
        
        data.write(Vector(self.users))
        
        return data.getvalue()
