from odoo import fields, models, api
from datetime import date
from odoo.exceptions import ValidationError
import re


class HMS_patient(models.Model):

    _name = "hms.patient"

    _sql_constraints = [
        ("Duplicate_Email", "UNIQUE(email)", "The email you entered already exists")
    ]

    first_name = fields.Char()
    last_name = fields.Char()
    birth_date = fields.Date()
    history = fields.Html()
    CR_Ratio = fields.Float()
    Blood_type = fields.Selection([('A', 'A'), ('B', 'B'), ('AB', 'AB'), ('O', 'O')])
    pcr = fields.Boolean()
    image = fields.Image()
    address = fields.Text()    
    department_id = fields.Many2one(comodel_name='hms.department')
    department_capacity = fields.Integer(related='department_id.capacity')
    doctor_id  = fields.Many2many(comodel_name='hms.doctor')
    states = fields.Selection([('st1', 'Undetermined'), ('st2', 'Good'), ('st3', 'Fair'), ('st4', 'Serious') ])
    history_states_log = fields.One2many('patient.history.log', 'patient_id')
    email = fields.Char()
    age = fields.Integer(compute = '_compute_age')

    @api.onchange('states')
    def create_states_log(self):
        for rec in self:
            vals = {
                'description':'State changed to %s'%(rec.states),
                'patient_id': rec.id
            }
            rec.env['patient.history.log'].create(vals)


    @api.onchange('age')
    def check_pcr(self):
        if self.age < 30 :
            self.pcr = True
            return {
                'warning': {
                    'title': ('PCR check'),
                    'message': 'PCR was Checked'
                }
            }
        else:
            self.pcr = False


    @api.depends('birth_date')
    def _compute_age(self):
        for rec in self:
            if rec.birth_date:
                today = date.today()
                rec.age = today.year - rec.birth_date.year - (
                        (today.month, today.day) < (rec.birth_date.month, rec.birth_date.day))
            else:
                rec.age = 1


    @api.constrains('email')
    def check_email(self):
        if self.email :

            pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'

            if not re.match(pattern, self.email):
                raise ValidationError('The email you entered is invalid')
