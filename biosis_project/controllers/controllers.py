# -*- coding: utf-8 -*-
from odoo import http

# class BiosisProject(http.Controller):
#     @http.route('/biosis_project/biosis_project/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/biosis_project/biosis_project/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('biosis_project.listing', {
#             'root': '/biosis_project/biosis_project',
#             'objects': http.request.env['biosis_project.biosis_project'].search([]),
#         })

#     @http.route('/biosis_project/biosis_project/objects/<model("biosis_project.biosis_project"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('biosis_project.object', {
#             'object': obj
#         })