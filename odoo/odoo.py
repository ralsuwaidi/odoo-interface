import xmlrpc.client
import os


class Odoo:
    def __init__(self) -> None:
        url = os.environ['URL']
        self.db = os.environ['DB']
        username = os.environ['USERNAME']
        self.password = os.environ['PASSWORD']
        
        common = xmlrpc.client.ServerProxy('{}/xmlrpc/2/common'.format(url))
        self.uid = common.authenticate(self.db, username, self.password, {})
        self.models = xmlrpc.client.ServerProxy('{}/xmlrpc/2/object'.format(url))



    def add_entry(self, entry: dict):
        """adds a generic entry to Odoo
        
        entry: a dictionary entry"""
        existing_entry = self._check_exist_individual()

        if len(existing_entry) > 0:
            return existing_entry[0]
        
        # add company if exists
        if entry['company'] != '':
            response = self.create_company(entry['company'])
            entry['parent_id'] = response['id']
        
        # remove company from dict as
        # it has been created already
        del entry['company']

        entry_id =  self.models.execute_kw(self.db, self.uid, self.password, 'res.partner', 'create', [entry])
        return {'id': entry_id}

    def get_entry(self, search_field: list, fields: list):
        """
        search_field: the search field as a list (eg '['is_company', '=,' 'True']')
        fields: list of fields to view https://github.com/odoo/odoo/blob/16.0/odoo/addons/base/models/res_partner.py
        """

        search = self.models.execute_kw(self.db, self.uid, self.password, 'res.partner', 'search', [search_field])
        return self.models.execute_kw(self.db, self.uid, self.password, 'res.partner', 'read', [search], {'fields': fields})

    def create_company(self, company_name):
        existing_company = self._check_exist_company(company_name)
        if len(existing_company) > 0:
            return existing_company[0]
        company_id = self.models.execute_kw(self.db, self.uid, self.password, 'res.partner', 'create', [{'name': company_name, 'is_company': True}])
        return {'id': company_id}


    def _check_exist_individual(self):
        """check if contact exists"""

        search_field = ['name', '=', self.name]
        return self.get_entry([search_field], ['id'])

    def _check_exist_company(self, company_name):
        """check if contact exists"""

        search_field = [['name', '=', company_name],['is_company', '=', True]]
        return self.get_entry(search_field, ['id'])


