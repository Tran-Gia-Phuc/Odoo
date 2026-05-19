# -*- coding: utf-8 -*-
from odoo import api, fields, models, tools, _
from odoo.exceptions import UserError, ValidationError

class ZooCreaturePlus(models.Model):
    _name = "zoo.creature"
    _inherit = "zoo.creature"
    _description = "Zoo Creature Plus"

    # 1. Chỉnh sửa field name: "Name" -> "Creature"
    name = fields.Char(string="Creature", required=True)

    # Bổ sung field type
    type = fields.Selection([
        ('mammal', 'Mammal'),
        ('bird', 'Bird'),
        ('reptile', 'Reptile'),
        ('amphibian', 'Amphibian'),
        ('fish', 'Fish'),
        ('insect', 'Insect'),
        ('other', 'Other')
    ], string='Type', default='other', required=True)

    # 2. Bổ sung field description (html)
    creature_description = fields.Html(string="Description")

    # 3. Bổ sung field One2many liên kết ngược về zoo.animal (qua field creature_id)
    animal_ids = fields.One2many(
        comodel_name='zoo.animal',
        inverse_name='creature_id',
        string='Animals'
    )

    # 4. Computed field đếm tổng số thú nuôi
    animal_count = fields.Integer(
        string="Animal Count",
        compute="_compute_animal_count",
        store=True
    )

    @api.depends('animal_ids')
    def _compute_animal_count(self):
        for record in self:
            record.animal_count = len(record.animal_ids)

    # 5. Method trả về danh sách tên thú nuôi
    def get_animal_names(self):
        self.ensure_one()
        return [animal.name for animal in self.animal_ids]