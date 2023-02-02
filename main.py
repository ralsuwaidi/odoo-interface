from odoo.individual import Individual

user = Individual(
    name= "test",
    email= "s@s.com",
    phone= "s",
    position= "UAE Editor",
    website= "sss.ss.s",
    company='s'
)

print(user.add_contact())