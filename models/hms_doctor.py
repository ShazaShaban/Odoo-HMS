from odoo import fields, models

class HMS_Doctor(models.Model):   #inherits from it

    _name = "hms.doctor"

    first_name  = fields.Char()
    last_name = fields.Char()
    image = fields.Image()
    department_id = fields.Many2one(comodel_name='hms.department')
    