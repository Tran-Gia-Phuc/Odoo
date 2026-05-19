from odoo import models, fields

class Student(models.Model):
    _name = 'demo.student'
    _description = 'Student'

    name = fields.Char(string="Name", required=True, index=True)
    age = fields.Integer(string="Age", default=18)
    note = fields.Text(string ="Note")
    fake = fields.Char(string="Fake") 
    
    class_id = fields.Many2one('demo.student_class', string="Class")  
    subject_ids = fields.Many2many(
    'demo.subject', 
    'student_subject_rel', # cùng tên relation
    'student_id',          # ✅ đảo lại: cột trỏ về student
    'subject_id',          # ✅ đảo lại: cột trỏ về subject
    string="Subjects"
)   
    name_age = fields.Char(string="Name and Age", compute="_compute_name_age")
    
    def _compute_name_age(self):
        for student in self:
            student.name_age = "%s (%s)" % (student.name, student.age)

    def test_create(self):
        self.env['demo.student'].create({
            'name': 'Pham Ngoc Bao Tran',
            'age': 19,
            'note': 'This is a test student.',
            'fake': 'Fake data'
        })
        
    def test_write(self):
        students = self.env['demo.student'].search([
            ('age', '=', 19)
        ])
        
        for student in students:
            student.write({
                'note': 'helo bao tran: %s' % student.name
            })
    
    def test_unlink(self):
        students = self.env['demo.student'].search([
            ('name', '=', 'a')
        ])
        students.unlink()
        
        