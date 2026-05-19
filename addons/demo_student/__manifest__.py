{
    'name': 'Demo Student',
    'version': '1.0',
    'depends': ['base'],
    'data': [
        'security/ir.model.access.csv',
            'wizard/assign_student_views.xml',
    'views/student_class_views.xml',
        'views/student_views.xml',
        'views/student_class_views.xml',
        'views/subject_views.xml',
    ],
    'installable': True,
    'application': True,
}