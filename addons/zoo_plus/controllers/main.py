import odoo
from odoo.addons.zoo.controllers.main import ZooAPI
from odoo.http import route
from odoo.http import request

import json
import logging
_logger = logging.getLogger(__name__)

class ZooAPIInherit(ZooAPI):
    @route(methods=['get', 'post'], auth='user') # '/api/zoo/animal/<id>'
    def get_animal_by_id(self, id, **kw):
        res = super(ZooAPIInherit, self).get_animal_by_id(id) # Response of json object
        _logger.warning(dir(res))
        _logger.warning(res)
        data = json.loads(res.get_data(as_text=True)) # https://werkzeug.palletsprojects.com/en/1.0.x/wrappers/#werkzeug.wrappers.BaseResponse.get_data
        record = request.env["zoo.animal"].sudo().search([('id', '=', int(id))], limit=1)
        if record:
            data["age"] = record.age
        # return data

        return request.make_response(
            json.dumps(data),
            headers=[('Content-Type', 'application/json')]
        )
        
    @route('/api/zoo/list/animal/', methods=['get', 'post'], auth='user'    )
    def get_animal_list(self, **kw):
        res = super(ZooAPIInherit, self).get_animal_list(**kw) # Response of json object
        _logger.warning(dir(res))
        _logger.warning(res)
        data = json.loads(res.get_data(as_text=True)) # https://werkzeug.palletsprojects.com/en/1.0.x/wrappers/#werkzeug.wrappers.BaseResponse.get_data
        
        records = request.env["zoo.animal"].sudo().search([])
        age_map = {r.name: r.age for r in records}
        for item in data:
            item["age"] = age_map.get(item["name"], 0)
        
        return request.make_response(
            json.dumps(data),
            headers=[('Content-Type', 'application/json')]
        )