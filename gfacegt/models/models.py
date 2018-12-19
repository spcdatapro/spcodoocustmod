# -*- coding: utf-8 -*-

from odoo import models, fields, api, exceptions
from odoo.tools.translate import _
from suds.client import Client
from xml.etree import cElementTree as ET

class gfacegt_config_res_company(models.Model):
    _name = 'res.company'
    _inherit = 'res.company'

    habilitargface = fields.Boolean(string='Habilitar GFACE GT', default=True)
    todoapruebasfe = fields.Boolean(string='Enviar todo a pruebas', default=False)

    #Campos para ambiente de prueba
    urltstfe = fields.Char(string='URL', size=500)
    usuariotstfe = fields.Char(string='Usuario', size=150)
    contraseniatstfe = fields.Char(string='Password', size=150)
    nitemisortstfe = fields.Char(string='NIT EFACE', size=150)
    establecimientotstfe = fields.Float(string='No. de establecimiento')
    idmaquinatstfe = fields.Char(string='ID Maquina', size=150)

    #Campos para ambiente de producción
    urlfe = fields.Char(string='URL', size=500)
    usuariofe = fields.Char(string='Usuario', size=150)
    contraseniafe = fields.Char(string='Password', size=150)
    nitemisorfe = fields.Char(string='NIT EFACE', size=150)
    establecimientofe = fields.Float(string='No. de establecimiento')
    idmaquinafe = fields.Char(string='ID Maquina', size=150)

class gfacegt_account_invoice(models.Model):
    _name = 'account.invoice'
    _inherit = 'account.invoice'

    @api.one
    @api.depends('state')
    def _onChange_state(self):
        #for invoice in self:
        empresa = self.company_id
        if empresa.habilitargface:
            if not self.confirmae and str(self.state).upper() == 'OPEN':
                urlws = empresa.urlfe if not empresa.todoapruebasfe else empresa.urltstfe
                usrws = empresa.usuariofe if not empresa.todoapruebasfe else empresa.usuariotstfe
                pwdws = empresa.contraseniafe if not empresa.todoapruebasfe else empresa.contraseniatstfe
                nitws = empresa.nitemisorfe if not empresa.todoapruebasfe else empresa.nitemisortstfe
                establecimientows = empresa.establecimientofe if not empresa.todoapruebasfe else empresa.establecimientotstfe
                tipodocws = 52
                idmaquinaws = empresa.idmaquinafe if not empresa.todoapruebasfe else empresa.idmaquinatstfe
                tiporespws = 'R'

                xmlstr = '<DocElectronico>'
                #Inicia el encabezado
                xmlstr+= '<Encabezado>'
                #Información del cliente
                xmlstr+= '<Receptor>'
                xmlstr+= '<NITReceptor>' + str(self.partner_id.vat).replace("-", "") + '</NITReceptor>'
                xmlstr+= '<Nombre>' + self.partner_id.name + '</Nombre>'
                xmlstr+= '<Direccion>' + str(self.partner_id.street) + '</Direccion>'
                xmlstr+= '</Receptor>'
                #Información del documento electrónico
                xmlstr+= '<InfoDoc>'
                xmlstr+= '<TipoVenta>B</TipoVenta>'
                xmlstr+= '<DestinoVenta>1</DestinoVenta>'
                #xmlstr+= '<Fecha>' + str(self.date_invoice) + '</Fecha>'
                xmlstr+= '<Fecha>' + fields.Date.from_string(str(self.date_invoice)).strftime('%d/%m/%Y') + '</Fecha>'
                xmlstr+= '<Moneda>1</Moneda>'
                xmlstr+= '<Tasa>1</Tasa>'
                xmlstr+= '<Referencia>' + str(self.id) + '</Referencia>'
                #xmlstr+= '<Reversion></Reversion>'
                xmlstr+= '</InfoDoc>'
                #Sumatorias del documento
                xmlstr+= '<Totales>'
                xmlstr+= '<Bruto>' + str(self.amount_total) + '</Bruto>'
                xmlstr+= '<Descuento>0</Descuento>'
                xmlstr+= '<Exento>0</Exento>'
                xmlstr+= '<Otros>0</Otros>'
                xmlstr+= '<Neto>' + str(self.amount_untaxed) + '</Neto>'
                xmlstr+= '<Isr>0</Isr>'
                xmlstr+= '<Iva>' + str(self.amount_tax) + '</Iva>'
                xmlstr+= '<Total>' + str(self.amount_total) + '</Total>'
                xmlstr+= '</Totales>'
                xmlstr+= '</Encabezado>'
                #Inicia detalle de la factura
                xmlstr+= '<Detalles>'

                for linea in self.invoice_line_ids:
                    xmlstr+= '<Productos>'
                    xmlstr+= '<Producto>' + str(linea.product_id.id) + '</Producto>'
                    xmlstr+= '<Descripcion>' + linea.product_id.name + '</Descripcion>'
                    xmlstr+= '<Medida>1</Medida>'
                    xmlstr+= '<Cantidad>' + str(linea.quantity) + '</Cantidad>'
                    xmlstr+= '<Precio>' + str(linea.price_unit) + '</Precio>'
                    xmlstr+= '<PorcDesc>0</PorcDesc>'
                    xmlstr+= '<ImpBruto>' + str(linea.price_total) + '</ImpBruto>'
                    xmlstr+= '<ImpDescuento>0</ImpDescuento>'
                    xmlstr+= '<ImpExento>0</ImpExento>'
                    xmlstr+= '<ImpOtros>0</ImpOtros>'
                    xmlstr+= '<ImpNeto>' + str(linea.price_subtotal) + '</ImpNeto>'
                    xmlstr+= '<ImpIsr>0</ImpIsr>'
                    xmlstr+= '<ImpIva>' + str(linea.price_total - linea.price_subtotal) + '</ImpIva>'
                    xmlstr+= '<ImpTotal>' + str(linea.price_total) + '</ImpTotal>'
                    xmlstr+= '</Productos>'

                xmlstr+= '</Detalles>'
                xmlstr+= '</DocElectronico>'

                self.xmlfactura = xmlstr

                #raise exceptions.Warning(_(self.xmlfactura + ' - URL = ' + str(urlws) + ' - Usr = ' + usrws + ' - Pwd = ' + pwdws + ' - NIT E = ' + nitws + ' - Estab = ' + str(establecimientows) + ' - TipoDoc = ' + str(tipodocws) + ' - IdMaq = ' + str(idmaquinaws) + ' - TipoResp = ' + tiporespws))

                client = Client(urlws)
                response = client.service.generaDocumento(usrws, pwdws, nitws, establecimientows, tipodocws, idmaquinaws, tiporespws, xmlstr)
                self.resultado = response

                root = ET.fromstring(response)
                if root.find('Serie') != None:
                    self.serie = root.find('Serie').text
                    self.preimpreso = root.find('Preimpreso').text
                    self.firmaelectronica = root.find('Firma').text
                    self.confirmae = True
                else:
                    self.serie = ""
                    self.preimpreso = ""
                    self.firmaelectronica = ""
                    self.confirmae = False
                    raise exceptions.Warning(_('El GFACE respondió con el siguiente error: ' + response))

    firmaelectronica = fields.Text(string='Firma electrónica', store=True, compute="_onChange_state")
    xmlfactura = fields.Text(string='XML de factura', store=True, compute="_onChange_state")
    serie = fields.Char(string='Serie', size=100, store=True, compute="_onChange_state")
    preimpreso = fields.Char(string='Preimpreso', size=100, store=True, compute="_onChange_state")
    resultado = fields.Text(string='Resultado GFACE', store=True, compute="_onChange_state")
    confirmae = fields.Boolean(string='Con firma', store=True, compute="_onChange_state")