from django.contrib.admin import AdminSite as DjangoAdminSite

from .models import SubjectConsent, SubjectLocator, Appointment
from .models import SubjectRequisition, SubjectVisit


class AdminSite(DjangoAdminSite):
    site_title = 'Cancer Subject'
    site_header = 'Cancer Subject'
    index_title = 'Cancer Subject'
    site_url = '/cancer_subject/list/'


cancer_subject_admin = AdminSite(name='cancer_subject_admin')

cancer_subject_admin.register(SubjectConsent)
cancer_subject_admin.register(SubjectLocator)
cancer_subject_admin.register(Appointment)
cancer_subject_admin.register(SubjectVisit)
cancer_subject_admin.register(SubjectRequisition)
