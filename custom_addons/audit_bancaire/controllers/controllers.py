# from odoo import http


# class AuditBancaire(http.Controller):
#     @http.route('/audit_bancaire/audit_bancaire', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/audit_bancaire/audit_bancaire/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('audit_bancaire.listing', {
#             'root': '/audit_bancaire/audit_bancaire',
#             'objects': http.request.env['audit_bancaire.audit_bancaire'].search([]),
#         })

#     @http.route('/audit_bancaire/audit_bancaire/objects/<model("audit_bancaire.audit_bancaire"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('audit_bancaire.object', {
#             'object': obj
#         })

