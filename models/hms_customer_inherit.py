from odoo import fields , models, api
from odoo.exceptions import  ValidationError, UserError
class HMS_Customers(models.Model):
    _inherit = 'res.partner'

    related_patient_id = fields.Many2one('hms.patient')

    _sql_constraints = [
        ("Duplicated_Email", "UNIQUE(related_patient_id)", "The email you entered is already assigned to another customer")
    ]


    def unlink(self):
        for rec in self :
            if rec.related_patient_id:
                raise UserError('This customer is already associated with another')
            else:
                super.unlink()