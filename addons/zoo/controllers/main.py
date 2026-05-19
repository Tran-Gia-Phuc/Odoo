import odoo
from odoo.tools import DEFAULT_SERVER_DATE_FORMAT, DEFAULT_SERVER_DATETIME_FORMAT
from odoo.http import request
import datetime
import json

import logging
_logger = logging.getLogger(__name__)

def convert_datetime(d):
    if d:
        return d.strftime(DEFAULT_SERVER_DATETIME_FORMAT) if isinstance(d, datetime.datetime) else d.strftime(DEFAULT_SERVER_DATE_FORMAT)
    else:
        return False

class ZooAPI(odoo.http.Controller):
    @odoo.http.route('/api/zoo/animal/<id>', type='http', auth='none', cors='*', csrf=False)
    def get_animal_by_id(self, id, **kw):
        env = request.env
        id = int(id)
        model = "zoo.animal"
        record = env[model].sudo().search([('id', '=', id)], limit=1)
        if record:
            res = {
                "name": record.name,
                "dob": convert_datetime(d=record.dob),
                "gender": record.gender,
                "feed_time": convert_datetime(d=record.feed_time),
            }
            _logger.warning(res)
            return request.make_json_response(res, status=200)
        else:
            return request.make_json_response({}, status=200)
        
    @odoo.http.route('/api/zoo/list/animal/', type='http', auth='none', cors='*', csrf=False)
    def get_animal_list(self, **kw):
        records = request.env["zoo.animal"].sudo().search([])
        
        if not records:
            return request.make_json_response([], status=200)
        
        res = []
        for record in records:
            res.append({
                "name": record.name,
                "dob": convert_datetime(d=record.dob),
                "gender": record.gender,
                "feed_time": convert_datetime(d=record.feed_time),
            })
        
        # ✅ return SAU khi vòng lặp chạy xong
        return request.make_json_response(res, status=200)
        
    @odoo.http.route('/api/zoo/list/animal_creature/', type='http', auth='none', cors='*', csrf=False)
    def get_animal_creature_list(self, **kw):
        env = request.env
        model = "zoo.creature"
        records = env[model].sudo().search([])
        res = []
        for record in records:
            res.append({
                "name": record.name,
                "environment": record.environment,
                "is_rare": record.is_rare,
                "animal_ids": [animal.id for animal in record.animal_ids],
            })
        _logger.warning(res)
        return request.make_json_response(res, status=200)