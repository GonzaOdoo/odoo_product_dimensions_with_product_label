{
    'name': 'Personalización de etiquetas',
    'version': '1.0',
    'summary': 'Modifica la vista de etiquetas de productos incluyendo Largo, Ancho, Alto, Volumen, Código de barra y Número de lote.',
    'author': 'Deglia',
    'depends': ['product', 'mrp'],
    'data': [
        'views/product_label_custom.xml',  
    ],
    'installable': True,
    'application': False,
    'license': 'LGPL-3',
}