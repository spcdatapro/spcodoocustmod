# -*- coding: utf-8 -*-
from odoo import http

# class Gfacegt(http.Controller):
#     @http.route('/gfacegt/gfacegt/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/gfacegt/gfacegt/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('gfacegt.listing', {
#             'root': '/gfacegt/gfacegt',
#             'objects': http.request.env['gfacegt.gfacegt'].search([]),
#         })

#     @http.route('/gfacegt/gfacegt/objects/<model("gfacegt.gfacegt"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('gfacegt.object', {
#             'object': obj
#         })