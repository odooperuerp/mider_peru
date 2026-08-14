# -*- coding: utf-8 -*-
{
    'name': 'Event Wallet Sale',
    'version': '17.0.1.0.0',
    'summary': 'Registro de eventos con monedero creando pedido sin factura',
    'author': 'BAIPERU ',
    # any module necessary for this one to work correctly
    'depends': ['event','sale','website_event'],

    # always loaded
    'data': [
        'views/event_templates.xml',
    ],
    # only loaded in demonstration mode
    'demo_xml': [],
    'active':True,
    'installable':True,
}
