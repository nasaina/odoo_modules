from odoo import models, fields, api

class AuditMission(models.Model):
	_name = 'audit.mission'
	_description = 'Mission d\'audit bancaire'

	name = fields.Char(string='Reference Mission', required=True)
	date_audit = fields.Date(string='Date Audit', required=True)
	entite_audit = fields.Char(string='Agence ou departement')
	auditeur_id = fields.Many2one('res.users', string='Auditeur', default=lambda self: self.env.user)
	statut = fields.Selection([
		('brouillon', 'Brouillon'),
		('en_cours', 'En cours'),
		('termine', 'Termine'),
	], string='Statut', default='brouillon')
	observations = fields.Text(string='Conclusion de l\'audit')

	def action_en_cours(self):
		self.statut = 'en_cours'

	def action_termine(self):
		self.statut = 'termine'
