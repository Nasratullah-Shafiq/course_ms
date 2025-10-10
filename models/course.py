from odoo import models, fields, api

class Course(models.Model):
    _name = 'course.course'
    _description = 'Course'

    name = fields.Char('Course Name', required=True)
    course_code = fields.Char('Code', required=True)
    category_id = fields.Many2one('course.category','Category')
    instructor_id = fields.Many2one('course.instructor','Instructor')
    duration = fields.Float('Duration (hours)')
    level = fields.Selection([('beginner','Beginner'),('intermediate','Intermediate'),('advanced','Advanced')], default='beginner')
    fee = fields.Monetary('Fee', currency_field='currency_id')
    currency_id = fields.Many2one('res.currency', string='Currency')
    student_count = fields.Integer('Enrolled Students', compute='_compute_student_count')
    session_ids = fields.One2many('course.session','course_id','Sessions')

    @api.depends('session_ids.enrollment_ids')
    def _compute_student_count(self):
        for record in self:
            count = 0
            for session in record.session_ids:
                count += len(session.enrollment_ids)
            record.student_count = count
