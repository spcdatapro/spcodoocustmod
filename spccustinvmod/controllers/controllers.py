# -*- coding: utf-8 -*-
from odoo import http

# class Spccustinvmod(http.Controller):
#     @http.route('/spccustinvmod/spccustinvmod/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/spccustinvmod/spccustinvmod/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('spccustinvmod.listing', {
#             'root': '/spccustinvmod/spccustinvmod',
#             'objects': http.request.env['spccustinvmod.spccustinvmod'].search([]),
#         })

#     @http.route('/spccustinvmod/spccustinvmod/objects/<model("spccustinvmod.spccustinvmod"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('spccustinvmod.object', {
#             'object': obj
#         })