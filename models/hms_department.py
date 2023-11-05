from odoo import fields, models

class HMS_department(models.Model):

    _name = "hms.department"

    name = fields.Char()
    capacity = fields.Integer()
    is_opened = fields.Boolean()
    patient_id = fields.One2many('hms.patient', 'department_id')
    doctor_id = fields.One2many( 'hms.doctor', 'department_id')
