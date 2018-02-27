from django.conf import settings
from django.conf.urls import url
from django.contrib import admin
from django.urls import path, re_path
from edc_constants.constants import UUID_PATTERN
from edc_dashboard import UrlConfig

from cancer_dashboard.views.checklist import EnrollmentCheckListBoardView

from .patterns import subject_identifier
from .views import SubjectListboardView, SubjectDashboardView


app_name = 'cancer_dashboard'

admin.autodiscover()


subject_listboard_url_config = UrlConfig(
    url_name='consent_listboard_url',
    view_class=SubjectListboardView,
    label='subject_listboard',
    identifier_label='subject_identifier',
    identifier_pattern=subject_identifier)
checklist_listboard_url_config = UrlConfig(
    url_name='checklist_listboard_url',
    view_class=EnrollmentCheckListBoardView,
    label='screening_listboard',
    identifier_label='screening_identifier',
    identifier_pattern=subject_identifier)
subject_dashboard_url_config = UrlConfig(
    url_name='dashboard_url',
    view_class=SubjectDashboardView,
    label='subject_dashboard',
    identifier_label='subject_identifier',
    identifier_pattern=subject_identifier)


# def listboard_urls():
#     urlpatterns = []
#     listboard_configs = [
#         ('consent_listboard_url', SubjectListboardView, 'listboard')]
#     for listboard_url_name, listboard_view_class, label in listboard_configs:
#         urlpatterns.extend([
#             re_path(r'^' + label + '/'
#                     '(?P<subject_identifier>' + subject_identifier + ')/'
#                     '(?P<page>\d+)/',
#                     listboard_view_class.as_view(), name=listboard_url_name),
#             re_path(r'^' + label + '/'
#                     '(?P<subject_identifier>' + subject_identifier + ')/',
#                     listboard_view_class.as_view(), name=listboard_url_name),
#             path(r'^' + label + '/<int:page>/',
#                  listboard_view_class.as_view(), name=listboard_url_name),
#             path(r'^' + label + '/',
#                  listboard_view_class.as_view(), name=listboard_url_name)])
#     return urlpatterns
#
#
# def dashboard_urls():
#     urlpatterns = []
#
#     dashboard_configs = [('dashboard_url', SubjectDashboardView, 'dashboard')]
#
#     for dashboard_url_name, dashboard_view_class, label in dashboard_configs:
#         urlpatterns.extend([
#             re_path(r'^' + label + '/'
#                     '(?P<subject_identifier>' + subject_identifier + ')/'
#                     '(?P<appointment>' + UUID_PATTERN.pattern + ')/',
#                     dashboard_view_class.as_view(), name=dashboard_url_name),
#             re_path(r'^' + label + '/'
#                     '(?P<subject_identifier>' + UUID_PATTERN.pattern + ')/',
#                     dashboard_view_class.as_view(), name=dashboard_url_name),
#             re_path(r'^' + label + '/'
#                     '(?P<subject_identifier>' + subject_identifier + ')/',
#                     dashboard_view_class.as_view(), name=dashboard_url_name),
#             re_path(r'^' + label + '/'
#                     '(?P<subject_identifier>' + subject_identifier + ')/'
#                     '(?P<schedule_name>' + 'schedule1' + ')/',
#                     dashboard_view_class.as_view(), name=dashboard_url_name),
#         ])
#     return urlpatterns
#
#
def checklist_listboard_urls():
    urlpatterns = []

    listboard_configs = [
        ('checklist_listboard_url', EnrollmentCheckListBoardView, 'checklist_listboard')]
    for listboard_url_name, listboard_view_class, label in listboard_configs:
        urlpatterns.extend([
            re_path(r'^' + label + '/'
                    '(?P<subject_identifier>' + subject_identifier + ')/'
                    '(?P<page>\d+)/',
                    listboard_view_class.as_view(), name=listboard_url_name),
            re_path(r'^' + label + '/'
                    '(?P<subject_identifier>' + subject_identifier + ')/',
                    listboard_view_class.as_view(), name=listboard_url_name),
            path(r'^' + label + '/<int:page>/',
                 listboard_view_class.as_view(), name=listboard_url_name),
            path(r'^' + label + '/',
                 listboard_view_class.as_view(), name=listboard_url_name)])
    return urlpatterns


# urlpatterns = listboard_urls() + screening_listboard_urls() + dashboard_urls()

urlpatterns = []
urlpatterns += subject_listboard_url_config.listboard_urls
urlpatterns += subject_dashboard_url_config.dashboard_urls
urlpatterns += checklist_listboard_url_config.listboard_urls
# urlpatterns += checklist_listboard_urls()

if settings.APP_NAME == 'cancer_dashboard':
    from .tests.admin import cancer_subject_admin
    urlpatterns = ([url(r'^admin/', cancer_subject_admin.urls)]
                   + urlpatterns)
