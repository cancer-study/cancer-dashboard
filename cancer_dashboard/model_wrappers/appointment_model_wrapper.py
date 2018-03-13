from django.apps import apps as django_apps
from edc_subject_dashboard import AppointmentModelWrapper as BaseAppointmentModelWrapper

from .subject_visit_model_wrapper import SubjectVisitModelWrapper


class AppointmentModelWrapper(BaseAppointmentModelWrapper):

    visit_model_wrapper_cls = SubjectVisitModelWrapper

    model = 'edc_appointment.appointment'
    next_url_name = django_apps.get_app_config(
        'cancer_dashboard').dashboard_url_name
    next_url_attrs = ['subject_identifier']
    querystring_attrs = ['subject_identifier']
    dashboard_url_name = django_apps.get_app_config(
        'cancer_dashboard').dashboard_url_name
