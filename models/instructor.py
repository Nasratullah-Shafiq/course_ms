from odoo import models, fields, api

class Instructor(models.Model):
    _name = 'course.instructor'
    _description = 'Instructor'


    name = fields.Char('Instructor Name', required=True)
    partner_id = fields.Many2one('res.partner','Partner')
    specialization = fields.Char('Specialization')
    course_ids = fields.One2many('course.course','instructor_id','Courses')
