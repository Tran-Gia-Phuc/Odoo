from odoo import models, fields, api
from odoo.exceptions import UserError   

class Class(models.Model):
    _name = 'demo.student_class'
    _description = 'Class'

    name = fields.Char(string="Class Name", required=True)
    student_ids = fields.One2many('demo.student', 'class_id', string="Students")
    
    
    def action_open_assign_wizard(self):
        return {
            'type': 'ir.actions.act_window',
            'name': 'Assign Students',
            'res_model': 'wizard.assign.student',
            'view_mode': 'form',
            'target': 'new',  # mở popup
            'context': {'default_class_id': self.id}
        }