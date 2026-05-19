# zoo_plus/models/pos_combo.py
from odoo import models, fields

class PosCombo(models.Model):
    _inherit = 'pos.combo'

    description = fields.Text(string='Mô tả')
    date_start = fields.Date(string='Ngày bắt đầu')
    date_end = fields.Date(string='Ngày kết thúc')
    
    