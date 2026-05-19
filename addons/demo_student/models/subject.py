from  odoo import models, fields, api
from odoo.exceptions import UserError   

class Subject(models.Model):
    _name = 'demo.subject'
    _description = 'Subject'

    name = fields.Char(string="Subject Name", required=True)
    student_ids = fields.Many2many(
        'demo.student',
        'student_subject_rel',
        'subject_id',
        'student_id',
        string="Students"
    )
    
    