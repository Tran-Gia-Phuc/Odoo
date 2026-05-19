# -*- coding: utf-8 -*-
from datetime import timedelta
from odoo import api, fields, models, tools, _
from odoo.exceptions import UserError, ValidationError

import requests

import logging
_logger = logging.getLogger(__name__)

class SaleOrder(models.Model):
    # khai bao thua ke:
    _name = "sale.order"
    _inherit = "sale.order"
    # them truong du lieu (field) vao model "sale.order"
    quick_note = fields.Char("Quick Note")
    priority = fields.Selection([('low', 'Low'), ('medium', 'Medium'), ('high', 'High')], default='low')
    last_support_date = fields.Date(default=lambda s: fields.Date.context_today(s)+timedelta(days=30))    