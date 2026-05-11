{
    'name': "audit_bancaire",

    'summary': "Short (1 phrase/line) summary of the module's purpose",

    'description': """
Long description of module's purpose
    """,

    'author': "Nasainarivelo Andrianarijaona",
    'website': "https://www.linkedin.com/in/nasainarivelo-andrianarijaona",

    'category': 'Uncategorized',
    'version': '0.1',

    'depends': ['base'],

    'data': [
        'security/ir.model.access.csv',
        'views/views.xml',
        'report/audit_mission_report.xml',
    ],
    'installable': True,
    'application': True,
}
