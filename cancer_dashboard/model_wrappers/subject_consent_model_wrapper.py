from django.apps import apps as django_apps
from django.core.exceptions import ObjectDoesNotExist

from edc_model_wrapper import ModelWrapper


class SubjectConsentModelWrapper(ModelWrapper):

    model = 'cancer_subject.subjectconsent'
    next_url_name = django_apps.get_app_config(
        'cancer_dashboard').listboard_url_name
    enrollment_checklist_model = 'cancer_subject.enrollmentchecklist'
#     next_url_attrs = ['subject_identifier']
#     querystring_attrs = ['subject_identifier']

    @property
    def enrollment_checklist_add_url(self):
        return self.enrollment_checklist_model_cls().get_absolute_url()

    @property
    def enrollment_checklist_model_cls(self):
        return django_apps.get_model(self.enrollment_checklist_model)

    @property
    def enrollment_checklist(self):

        try:
            enrollment_checklist_obj = self.enrollment_checklist_model_cls.objects.get(
                subject_identifier=self.object.subject_identifier)
        except ObjectDoesNotExist:
            enrollment_checklist_obj = None
        return enrollment_checklist_obj
