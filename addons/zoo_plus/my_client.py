from xml_rpc import XMLRPC_API, myprint

import ssl
ssl._create_default_https_context = ssl._create_unverified_context

# please change the credential!
ODOO_BACKEND = 'http://localhost:8069'
ODOO_DB      = 'test'
ODOO_USER    = 'giaphuc031204@gmail.com'
# ODOO_PASS    = 'Phucsida98'
ODOO_PASS    = '0eb1dd26686f71aea695a674f5fee9a01fb57be2'

def main():
    client = XMLRPC_API(url=ODOO_BACKEND, db=ODOO_DB, username=ODOO_USER, password=ODOO_PASS)
    print(client.call(model_name="zoo.animal", method="get_basic_animal_info", params=[False, 3]))
    # {'name': 'Polar Bear', 'gender': 'female', 'age': 5, 'feed_visitor_message': ''}

if __name__ == "__main__":
    main()