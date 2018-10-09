from django.contrib.admin import AdminSite as DjangoAdminSite

from .models import SubjectConsent, SubjectLocator
from .models import SubjectRequisition, SubjectVisit, SubjectScreening


class AdminSite(DjangoAdminSite):
    site_title = 'Cancer Subject'
    site_header = 'Cancer Subject'
    index_title = 'Cancer Subject'
    site_url = '/administration/'


cancer_test_admin = AdminSite(name='cancer_test_admin')

cancer_test_admin.register(SubjectScreening)
cancer_test_admin.register(SubjectConsent)
cancer_test_admin.register(SubjectLocator)
cancer_test_admin.register(SubjectVisit)
cancer_test_admin.register(SubjectRequisition)
