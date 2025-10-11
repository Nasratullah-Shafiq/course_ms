from odoo import models, fields, api

class Payment(models.Model):
    _name = 'course.payment'
    _description = 'Payment'

    student_id = fields.Many2one('course.student','Student')
    course_id = fields.Many2one('course.course','Course')
    amount = fields.Monetary('Amount', currency_field='currency_id')
    currency_id = fields.Many2one('res.currency','Currency')
    payment_date = fields.Date('Payment Date')
    method = fields.Selection([('cash','Cash'),('card','Card'),('bank','Bank Transfer')], default='cash')
    state = fields.Selection([('draft','Draft'),('paid','Paid'),('cancelled','Cancelled')], default='draft')
