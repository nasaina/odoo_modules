from odoo import models, fields, api

class AuditMission(models.Model):
	_name = 'audit.mission'
	_description = 'Bank audit mission'

	name = fields.Char(string='Mission Reference', required=True)
	date_audit = fields.Date(string='Audit Date', required=True, default=fields.Date.today)
	date_fin = fields.Date(string='End Date')
	entite_audit = fields.Char(string='Branch or Department')
	auditeur_id = fields.Many2one('res.users', string='Auditor', default=lambda self: self.env.user)
	statut = fields.Selection([
		('brouillon', 'Draft'),
		('en_cours', 'In Progress'),
		('termine', 'Done'),
	], string='Status', default='brouillon')
	observations = fields.Text(string='Audit Conclusion')

	def action_en_cours(self):
		"""Set mission status to In Progress."""
		self.statut = 'en_cours'

	def action_termine(self):
		"""Set mission status to Done and record the end date."""
		self.statut = 'termine'
		self.date_fin = fields.Date.today()

	def action_brouillon(self):
		"""Reset mission status to Draft."""
		self.statut = 'brouillon'

	def pdf_generate(self):
		"""Generate and download the audit mission PDF report."""
		return self.env.ref('audit_bancaire.action_report_audit_mission').report_action(self)