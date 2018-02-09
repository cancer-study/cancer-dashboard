from django.apps import apps as django_apps
from django.core.exceptions import ObjectDoesNotExist

from edc_model_wrapper import ModelWrapper


class CrfModelWrapper(ModelWrapper):

    next_url_name = django_apps.get_app_config(
        'cancer_dashboard').dashboard_url_name
    next_url_attrs = ['appointment', 'subject_identifier']
    querystring_attrs = ['subject_visit', 'regimen']

    @property
    def subject_visit(self):
        return str(self.object.subject_visit.id)

    @property
    def appointment(self):
        return str(self.object.subject_visit.appointment.id)

    @property
    def subject_identifier(self):
        return self.object.subject_visit.subject_identifier
