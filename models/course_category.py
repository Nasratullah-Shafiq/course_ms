from odoo import models, fields, api

class CourseCategory(models.Model):
    _name = 'course.category'
    _description = 'Course Category'


    name = fields.Char('Category Name', required=True)
    description = fields.Text('Description')
    course_count = fields.Integer('Total Courses', compute='_compute_course_count')

    @api.depends('course_ids')
    def _compute_course_count(self):
        for record in self:
            record.course_count = len(record.course_ids)

    course_ids = fields.One2many('course.course','category_id','Courses')
