# -*- coding: utf-8 -*-
from odoo import api, fields, models, tools, _
from odoo.exceptions import UserError, ValidationError

import logging
_logger = logging.getLogger(__name__)

class ToyClearWizard(models.TransientModel):
    _name = "zoo.toy.clear.wizard"
    _description = "Clear toy"

    name = fields.Char('Name')

    def clear_toy(self):
        ids = self.env.context['active_ids'] # selected record ids        
        zoo_animals = self.env["zoo.animal"].browse(ids)
        # https://www.odoo.com/documentation/14.0/reference/orm.html#create-update
        data = {
            "toy_ids": [(5, 0, 0)]
        }
        zoo_animals.write(data)
    