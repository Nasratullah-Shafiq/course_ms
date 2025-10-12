from odoo import models, fields, api


# class Student(models.Model):
#     _name = 'course.student'
#     _description = 'Student'
#
#     name = fields.Char('Student Name', required=True)
#     partner_id = fields.Many2one('res.partner','Partner')
#     email = fields.Char('Email')
#     phone = fields.Char('Phone')
#     status = fields.Selection([('active','Active'),('inactive','Inactive')], default='active')
#     enrollment_ids = fields.One2many('course.enrollment','student_id','Enrollments')

class CourseStudent(models.Model):
    _name = 'course.student'
    _description = 'Student'
    _inherit = ['mail.thread']

    name = fields.Char(string='Full Name', required=True, tracking=True)
    student_ref = fields.Char(string='Student ID', readonly=True, copy=False)
    partner_id = fields.Many2one('res.partner', string='Partner')
    email = fields.Char()
    phone = fields.Char()
    gender = fields.Selection([('male', 'Male'), ('female', 'Female'), ('other', 'Other')])
    dob = fields.Date('Date of Birth')
    address = fields.Text()
    image = fields.Image()
    enrollment_ids = fields.One2many('course.enrollment', 'student_id', string='Enrollments')
    status = fields.Selection([('active', 'Active'), ('graduated', 'Graduated'), ('dropped', 'Dropped')],
                              default='active')

    @api.model
    def create(self, vals):

        if not vals.get('student_ref'):
            seq = self.env['ir.sequence'].next_by_code('course.student')
            vals['student_ref'] = seq

        # create partner if not provided
        if not vals.get('partner_id') and vals.get('name'):
            partner = self.env['res.partner'].create({'name': vals.get('name')})
            vals['partner_id'] = partner.id
            return super().create(vals)

    def write(self, vals):
        # sync partner name
        res = super().write(vals)
        for rec in self:
            if rec.partner_id and rec.partner_id.name != rec.name:
                rec.partner_id.name = rec.name
        return res
