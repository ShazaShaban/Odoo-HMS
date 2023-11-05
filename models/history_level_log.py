from odoo import fields, models, api

class Patient_History_Log(models.Model):

    _name = "patient.history.log"

    description = fields.Char(required = True)
    patient_id = fields.Many2one('hms.patient')
    