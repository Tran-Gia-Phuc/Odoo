# -*- coding: utf-8 -*-
from odoo import api, fields, models, tools, _
from odoo.exceptions import UserError, ValidationError

import logging
_logger = logging.getLogger(__name__)

class CageUpdateWizard(models.TransientModel):
    _name = "zoo.cage.update.wizard"
    _description = "Update cage"

    cage_id = fields.Many2one('zoo.cage', string='Cage', required=True)    

    def update_cage(self):
        ids = self.env.context['active_ids'] # selected record ids        
        zoo_animals = self.env["zoo.animal"].browse(ids)
        # https://www.odoo.com/documentation/14.0/reference/orm.html#create-update
        data = {
            "cage_id": self.cage_id.id,
        }
        zoo_animals.write(data)
    