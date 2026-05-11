{
    'name': "Bank Audit",

    'summary': "Manage bank audit missions with status workflow and PDF report generation.",

    'description': """
        Custom module for managing bank audit missions.
        Features:
        - Track audit missions (draft → in progress → done)
        - Assign auditors and audited entities
        - Automatically record the end date on completion
        - Generate a PDF audit report
    """,

    'author': "Nasainarivelo Andrianarijaona",
    'website': "https://www.linkedin.com/in/nasainarivelo-andrianarijaona",

    'category': 'Accounting',
    'version': '19.0.0.1',

    'depends': ['base'],

    'data': [
        'security/ir.model.access.csv',
        'views/views.xml',
        'report/audit_mission_report.xml',
    ],
    'installable': True,
    'application': True,
}
