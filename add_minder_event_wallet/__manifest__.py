# -*- coding: utf-8 -*-
{
    'name': 'Minder Event Wallet Integration',
    'version': '17.0.1.0.0',
    'category': 'Website/Website',
    'summary': 'Muestra el saldo del monedero en la web y permite pagar entradas de eventos.',
    'description': """
        - Agrega el saldo de loyalty.card (eWallet) en la cabecera del sitio web.
        - Intercepta el registro a eventos para descontar el saldo del monedero si el ticket es tipo "Saldo".
    """,
    'author': 'BAI PERU',
    'depends': [
        'website', 
        'event', 
        'website_event', 
        'loyalty'
    ],
    'data': [
        'views/website_templates.xml',
    ],
    'installable': True,
    'application': False,
    'license': 'LGPL-3',
}