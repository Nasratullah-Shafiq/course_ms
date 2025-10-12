from odoo import models, fields, api

class Session(models.Model):
    _name = 'course.session'
    _description = 'Course Session'

    name = fields.Char('Session Name', required=True)
    course_id = fields.Many2one('course.course','Course')
    instructor_id = fields.Many2one('course.instructor','Instructor')
    start_datetime = fields.Datetime('Start Time')
    end_datetime = fields.Datetime('End Time')
    location = fields.Char('Location')
    enrollment_ids = fields.One2many('course.enrollment','session_id','Enrollments')
