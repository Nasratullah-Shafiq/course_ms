from odoo import models, fields

class CourseMaterial(models.Model):
    _name = 'course.material'
    _description = 'Course Material'

    name = fields.Char('Material Name', required=True)
    course_id = fields.Many2one('course.course','Course', required=True)
    material_type = fields.Selection([('pdf','PDF'),('video','Video'),('doc','Document')], default='pdf')
    file = fields.Binary('File')

