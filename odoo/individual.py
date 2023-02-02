from dataclasses import dataclass
from odoo.odoo import Odoo
from typing import Optional

@dataclass
class Individual(Odoo):
    """Class for saving user data"""

    def __init__(self,  name,  email, position, website, mobile="", phone="", company=""):
        super().__init__()
        self.name = name
        self.phone = phone
        self.email = email
        self.position = position
        self.website = website
        self.mobile = mobile
        self.company = company


    def to_dict(self):
        return {
            "name": self.name or '',
            "phone": self.phone or '',
            "mobile": self.mobile or '',
            "email": self.email or '',
            "function": self.position or '',
            "website": self.website or '',
            "company": self.company or ''
        }




    def add_contact(self):
        return self.add_entry(self.to_dict())