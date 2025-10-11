from odoo import models, fields

class Exam(models.Model):
    _name = 'course.exam'
    _description = 'Exam'

    name = fields.Char('Exam Name', required=True)
    course_id = fields.Many2one('course.course','Course')
    exam_date = fields.Datetime('Exam Date')
    total_marks = fields.Float('Total Marks')
    result_ids = fields.One2many('course.result','exam_id','Results')
