# zoo/creature_client.py

from xml_rpc import XMLRPC_API, myprint
import ssl
ssl._create_default_https_context = ssl._create_unverified_context

# my_client.py
ODOO_BACKEND = 'http://localhost:8069'
ODOO_DB      = 'test'
ODOO_USER    = 'giaphuc031204@gmail.com'
# ODOO_PASS    = 'Phucsida98'
ODOO_PASS    = '0eb1dd26686f71aea695a674f5fee9a01fb57be2'

def main():
    client = XMLRPC_API(
        url=ODOO_BACKEND,
        db=ODOO_DB,
        username=ODOO_USER,
        password=ODOO_PASS
    )

    # ── CREATE ──────────────────────────────
    id = client.create(
        model_name='zoo.creature',
        data_dict={
            'name': 'Dragon',           # bắt buộc
            'environment': 'sky',       # water | ground | sky
            'is_rare': True,
        }
    )
    print(f"Created creature @ {id}")

    # ── READ ────────────────────────────────
    myprint(
        client.read(
            model_name='zoo.creature',
            conditions=[('id', '>=', 1)],
            params={'fields': ['name', 'environment', 'is_rare']}
        ),
        title='Zoo Creatures'
    )

    # ── UPDATE ──────────────────────────────
    client.update(
        model_name='zoo.creature',
        id_list=[id],
        new_data_dict={
            'name': 'Dragon Updated',
            'is_rare': False,
        }
    )
    print(f"Updated creature @ {id}")

    # ── DELETE ──────────────────────────────
    client.delete(
        model_name='zoo.creature',
        id_list=[id]
    )
    print(f"Deleted creature @ {id}")

if __name__ == '__main__':
    main()