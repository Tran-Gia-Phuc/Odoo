# -*- coding: utf-8 -*-
from odoo import api, fields, models, tools, _
from odoo.exceptions import UserError, ValidationError


import requests

import logging
_logger = logging.getLogger(__name__)

# class ZooAnimal(models.Model):
#     _inherit = "zoo.animal"
#     _name = "zoo.animal"
#     _description = "Extended Zoo Animal"
    
#     is_feed_by_visitor = fields.Boolean(string="Is Feed By Visitor")
#     age = fields.Integer(string="Age", compute="_compute_age", store=True)
#     feed_visitor_message = fields.Char('Feeding Message', default='')
#     @api.onchange('is_feed_by_visitor')
#     def _update_feed_visitor_message(self):
#         for record in self:
#             if record.is_feed_by_visitor:
#                 record.feed_visitor_message = "This animal can be fed by visitors."
#             else:
#                 record.feed_visitor_message = "This animal cannot be fed by visitors."  
                
#     def get_basic_animal_info(self):
#         return {
#             "name": self.name,
#             "gender": self.gender,
#             "age": self.age,
#             "is_feed_by_visitor": self.is_feed_by_visitor,
#         }

#     @api.depends('dob')
#     def _compute_age(self):
#         for record in self:
#             if record.dob:
#                 today = fields.Date.today()
#                 age = today.year - record.dob.year - ((today.month, today.day) < (record.dob.month, record.dob.day))
#                 record.age = age
#             else:
#                 record.age = 0
                
#     def send_sms(self):
#         if not self.description:
#             raise ValidationError("Cannot send SMS due to empty description!")
#         # https://esms.vn/SMSApi/ApiDetail
#         url = "http://rest.esms.vn/MainService.svc/json/SendMultipleMessage_V4_post_json/"
#         data = {
#             "ApiKey": "9DF7A8FDDC5B8BEB99618CA9CC67DB", # <- registered to esms.vn
#             "Content": self.description,
#             "Phone": "0349684064",
#             "SecretKey": "1A1D459D80F3B633300D7F79B1BEE1", # <- registered to esms.vn
#             "IsUnicode": 1,
#             # "Brandname": "minhng.info",
#             "SmsType": 8,
#             "Sandbox": 1, # 0=production (send real SMS), 1=sandbox mode (no SMS sent)
#         }
#         response = requests.post(url, json=data)
#         # curl "http://rest.esms.vn/MainService.svc/json/GetSendStatus?RefId=be1eef90-c174-4c52-ada5-c3f0e8b9cddb127&ApiKey=9DF7A8FDDC5B8BEB99618CA9CC67DB&SecretKey=1A1D459D80F3B633300D7F79B1BEE1"
#         raise UserError(str(response.json()))
    
    
class ZooAnimalPlus(models.Model):
    _name = "zoo.animal"
    _inherit = "zoo.animal"
    _description = "Extends zoo animal model"

    # modify existing fields
    name = fields.Char('Animal Name (+)')
    gender = fields.Selection(selection_add=[('other', 'Other')], default='female', ondelete={'other': lambda recs: recs.write({'gender': 'male'})})
    
    # add new field
    is_feed_by_visitor = fields.Boolean('Is Feed By Visitor', default=False)
    feed_visitor_message = fields.Char('Feeding Message', default='')
    
    @api.onchange('is_feed_by_visitor')
    def _update_feed_visitor_message(self):
        if self.is_feed_by_visitor:
            self.feed_visitor_message = "Allow to feed the animal"
        else:
            self.feed_visitor_message = "Do not feed the animal!"
    
    # add new method
    def get_basic_animal_info(self, id):
        record = self.browse(id)
        return str({
            "name": record.name,
            "gender": record.gender,
            "age": record.age,
            "feed_visitor_message": record.feed_visitor_message,
        })
    
    def send_sms(self):
        if not self.description:
            raise ValidationError("Cannot send SMS due to empty description!")
        # https://esms.vn/SMSApi/ApiDetail
        url = "http://rest.esms.vn/MainService.svc/json/SendMultipleMessage_V4_post_json/"
        data = {
            "ApiKey": "9DF7A8FDDC5B8BEB99618CA9CC67DB", # <- registered to esms.vn
            "Content": self.description,
            "Phone": "0349684064",
            "SecretKey": "1A1D459D80F3B633300D7F79B1BEE1", # <- registered to esms.vn
            "IsUnicode": 1,
            # "Brandname": "minhng.info",
            "SmsType": 8,
            "Sandbox": 1, # 0=production (send real SMS), 1=sandbox mode (no SMS sent)
        }
        response = requests.post(url, json=data)
        # curl "http://rest.esms.vn/MainService.svc/json/GetSendStatus?RefId=be1eef90-c174-4c52-ada5-c3f0e8b9cddb127&ApiKey=9DF7A8FDDC5B8BEB99618CA9CC67DB&SecretKey=1A1D459D80F3B633300D7F79B1BEE1"
        raise UserError(str(response.json()))