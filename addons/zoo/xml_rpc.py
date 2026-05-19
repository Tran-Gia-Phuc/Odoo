import xmlrpc.client

# my_client.py
ODOO_BACKEND = 'http://localhost:8069'
ODOO_DB      = 'test'
ODOO_USER    = 'giaphuc031204@gmail.com'
# ODOO_PASS    = 'Phucsida98'
ODOO_PASS = '0eb1dd26686f71aea695a674f5fee9a01fb57be2'


def myprint(data_list, title=''):
    if title:
        print(title)
    for line in data_list:
        print('-', line)
    pass

# https://www.odoo.com/documentation/17.0/developer/reference/external_api.html
# https://www.odoo.com/documentation/17.0/developer/howtos/web_services.html
class XMLRPC_API():
    def __init__(self, url, db, username='admin', password='b5c835566552c23c335ba576e045a5e50d87b3a3'):
        self.url = url
        self.db = db
        self.username = username
        self.password = password
        common = xmlrpc.client.ServerProxy('{}/xmlrpc/2/common'.format(self.url))
        self.uid = common.authenticate(self.db, self.username, self.password, {})
        self.models = xmlrpc.client.ServerProxy('{}/xmlrpc/2/object'.format(self.url))
        pass

    # get fields names of the model
    def get_fields(self, model_name, required=False):
        data = self.models.execute_kw(self.db, 
            self.uid, 
            self.password, 
            model_name, 
            'fields_get',
            [], {'attributes': ['string', 'type', 'required', 'readonly']})
        
        if required:
            key_list = list(data.keys())
            for k in key_list:
                if not data[k].get('required', False):
                    data.pop(k)
                pass
        return data

    def search(self, model_name, conditions=[()]):
        return self.models.execute_kw(self.db, self.uid, self.password,
            model_name, 
            'search',
            [conditions])  

    # Create
    def create(self, model_name, data_dict):
        """
        Eg.
            model_name: 'res.users'
            data_dict: { 'name': "Minh", 'age': 27 }
        """
        id = self.models.execute_kw(self.db, self.uid, self.password, model_name, 'create', [data_dict])
        return id

    # Read
    def read(self, model_name, conditions=[()], params={}):
        """
        Eg.
            model_name: 'res.users'
            conditions: [('id', '>', 1)]
            params: {'fields': ['name', 'country_id', 'comment'], 'limit': 5}
        """
        return self.models.execute_kw(self.db, self.uid, self.password,
            model_name, 
            'search_read',
            [conditions],
            params)       
    
    # Update
    def update(self, model_name, id_list, new_data_dict):
        """
        Eg.
            model_name: 'res.users'
            id_list: [7]
            new_data_dict: { 'name': "Newer partner", 'age': 27 }
        """
        self.models.execute_kw(self.db, 
            self.uid, 
            self.password, 
            model_name, 
            'write', 
            [id_list, new_data_dict])

    # Delete
    def delete(self, model_name, id_list):
        self.models.execute_kw(self.db, self.uid, self.password, model_name, 'unlink', [id_list])
        pass

    # Soft delete
    def soft_delete(self, model_name, id_list):
        self.update(model_name, id_list, {
            'active': False,
        })

    # Aug 01, 2019
    def call(self, model_name, method, params=[]):
        return self.models.execute_kw(self.db, self.uid, self.password, model_name, method, params)

    def call2(self, model_name, method, param1, param2):
        return self.models.execute_kw(self.db, self.uid, self.password, model_name, method, param1, param2)

def main():
    client = XMLRPC_API(url=ODOO_BACKEND, db=ODOO_DB, username=ODOO_USER, password=ODOO_PASS)

    # list vendor accounts
    myprint(client.read(model_name='zoo.animal', 
        conditions=[('id', '>=', 1)], 
        params={ 'fields': ['name', 'dob'], }), title='Read Zoo Animal')
    
    myprint(client.call2(model_name="zoo.animal", method="search_read", param1=[[('id', '>=', 1)]], param2={}), title='General Call')

    client.create(model_name="zoo.animal", data_dict={"name": "Minh"})
    print("Created new animal")

    client.update(model_name="zoo.animal", id_list=[1], new_data_dict={"name": "MKyz"})
    print("Update new animal")

    pass

if __name__ == '__main__':
    main()