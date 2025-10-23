from odoo import models, fields, api
from odoo.exceptions import ValidationError

class Result(models.Model):
    _name = 'course.result'
    _description = 'Result'

    exam_id = fields.Many2one('course.exam','Exam')
    student_id = fields.Many2one('course.student','Student')
    marks_obtained = fields.Float('Marks Obtained')
    grade = fields.Selection([('A','A'),('B','B'),('C','C'),('D','D'),('F','F')],'Grade')

    @api.constrains('marks_obtained','exam_id')
    def _check_marks(self):
        for record in self:
            if record.marks_obtained > record.exam_id.total_marks:
                raise ValidationError('Marks cannot exceed total marks.')

