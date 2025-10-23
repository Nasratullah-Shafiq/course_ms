from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


#
# class Enrollment(models.Model):
#     _name = 'course.enrollment'
#     _description = 'Enrollment'
#
#     student_id = fields.Many2one('course.student','Student', required=True)
#     course_id = fields.Many2one('course.course','Course', required=True)
#     session_id = fields.Many2one('course.session','Session')
#     enroll_date = fields.Date('Enrollment Date')
#     state = fields.Selection([('draft','Draft'),('enrolled','Enrolled'),('cancelled','Cancelled')], default='draft')
#
#     @api.constrains('student_id','course_id')
#     def _check_unique_enrollment(self):
#         for record in self:
#             existing = self.search([('student_id','=',record.student_id.id),('course_id','=',record.course_id.id),('id','!=',record.id)])
#             if existing:
#                 raise ValidationError('Student already enrolled in this course.')


class CourseEnrollment(models.Model):
    _name = 'course.enrollment'

    _description = 'Enrollment'
    _inherit = ['mail.thread']

    student_id = fields.Many2one('course.student', string='Student', required=True)
    course_id = fields.Many2one('course.course', string='Course', required=True)
    enroll_date = fields.Date(default=fields.Date.context_today)
    state = fields.Selection([('enrolled', 'Enrolled'), ('completed', 'Completed'), ('cancelled', 'Cancelled')],
                             default='enrolled', tracking=True)
    grade = fields.Char()
    attendance_percent = fields.Float(digits=(5, 2))
    fees_paid = fields.Boolean(default=False)
    invoice_id = fields.Many2one('account.move', string='Invoice')

    _sql_constraints = [
        ('student_course_unique', 'unique(student_id,course_id)', 'Student is already enrolled in this course')
    ]

    def action_mark_completed(self):
        for rec in self:
            rec.state = 'completed'

    def action_cancel(self):
        for rec in self:
            if rec.invoice_id and rec.invoice_id.state == 'posted':
                raise ValidationError(_('Cannot cancel enrollment when invoice is posted. Cancel invoice first.'))
                rec.state = 'cancelled'

    def action_create_invoice(self):
        """Create an account.move invoice for the enrollment's course fee."""

        AccountMove = self.env['account.move']
        for rec in self:
            if not rec.course_id or not rec.course_id.fee:
                raise ValidationError(_('Course has no fee defined.'))


    # find/create partner
    # partner = rec.student_id.partner_id
    #     if not partner:
    #     partner = self.env['res.partner'].create({'name': rec.student_id.name})
    #     rec.student_id.partner_id = partner
    #
    # invoice_vals = {
    #     'partner_id': partner.id,
    #     'move_type': 'out_invoice',
    #     'invoice_date': fields.Date.context_today(self),
    #     'invoice_line_ids': [(0, 0, {
    #         'name': rec.course_id.name,
    #         'quantity': 1,
    #         'price_unit': rec.course_id.fee,
    #         'product_id': False,
    #     })]
    # }
    # invoice = AccountMove.create(invoice_vals)
    # rec.invoice_id = invoice.id
    # rec.message_post(body=_('Invoice created: %s') % (invoice.name or invoice.id,))
    #
    # def action_register_payment(self):
    #     for rec in self:
    #         if not rec.invoice_id:
    #             raise ValidationError(_('No invoice linked. Please create invoice first.'))
    #
    # if rec.invoice_id.state != 'posted':
    #     rec.invoice_id.action_post()
