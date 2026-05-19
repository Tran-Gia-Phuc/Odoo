from odoo import models, fields

class AssignStudent(models.TransientModel):
    _name = 'wizard.assign.student'
    _description = 'Assign Student to Class'

    class_id = fields.Many2one('demo.student_class', string="Class")
    student_ids = fields.Many2many(
        'demo.student',
        domain=[('class_id', '=', False)],
        string="Students"
    )

    def action_assign(self):
        for student in self.student_ids:
            student.class_id = self.class_id