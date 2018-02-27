from django.apps import apps as django_apps
from django.core.exceptions import ObjectDoesNotExist
from django.utils.safestring import mark_safe
from edc_consent import ConsentModelWrapperMixin

from edc_model_wrapper import ModelWrapper

from .subject_consent_model_wrapper import SubjectConsentModelWrapper


class EnrollmentChecklistModelWrapper(ConsentModelWrapperMixin, ModelWrapper):

    consent_model_wrapper_cls = SubjectConsentModelWrapper
    model = 'cancer_subject.subjecteligibility'
    next_url_name = django_apps.get_app_config(
        'cancer_dashboard').checklist_listboard_url_name
    next_url_attrs = ['subject_identifier']
    querystring_attrs = ['gender']

    @property
    def html_reason(self):
        if not self.eligible:
            html = '<BR>'.join(self.object.reasons_ineligible.split(','))
            return mark_safe('<BR>'.join(['No:', html]))
        else:
            return 'Yes.'

    @property
    def consented(self):
        return self.object.subject_identifier

    @property
    def create_consent_options(self):
        options = super().create_consent_options
        options.update(screening_identifier=self.object.screening_identifier)
        return options

    @property
    def consent(self):
        """Returns a wrapped saved or unsaved consent.
        """
        model_cls = django_apps.get_model(self.consent_model)
        try:
            consent = model_cls.objects.get(
                screening_identifier=self.object.screening_identifier)
        except ObjectDoesNotExist:
            consent = self.consent_object.model(**self.create_consent_options)
        return self.consent_model_wrapper_cls(model_obj=consent)
