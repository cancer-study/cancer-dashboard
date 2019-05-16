from django import template
from django.conf import settings

register = template.Library()


@register.inclusion_tag('cancer_dashboard/buttons/screening_button.html')
def screening_button(model_wrapper):
    title = ['Add subject\' screening form.']
    return dict(
        subject_identifier=model_wrapper.object.subject_identifier,
        add_subject_screening_href=model_wrapper.subject_screening.href,
        subject_screening_model_obj=model_wrapper.subject_screening_model_obj,
        title=' '.join(title))


@register.inclusion_tag('cancer_dashboard/buttons/subject_locator_button.html')
def subject_locator_button(model_wrapper):
    title = ['Edit Locator.']
    return dict(
        subject_identifier=model_wrapper.subject_locator.subject_identifier,
        add_subject_locator_href=model_wrapper.subject_locator.href,
        subject_locator_model_obj=model_wrapper.subject_locator_model_obj,
        title=' '.join(title))

# @register.inclusion_tag('cancer_dashboard/buttons/eligibility_button.html')
# def eligibility_button(subject_screening_model_wrapper):
#     comment = []
#     obj = subject_screening_model_wrapper.object
#     tooltip = None
# #     if not obj.is_consented:
# #         comment = obj.reasons_ineligible.split(',')
# #     comment = list(set(comment))
# #     comment.sort()
#     return dict(eligible=obj.is_consented, comment=comment, tooltip=tooltip)


@register.inclusion_tag('cancer_dashboard/buttons/consent_button.html')
def consent_button(model_wrapper):
    title = ['Consent subject to participate.']
    consent_version = model_wrapper.version
    return dict(
        screening_identifier=model_wrapper.object.screening_identifier,
        add_consent_href=model_wrapper.href,
        consent_version=consent_version,
        title=' '.join(title))


@register.inclusion_tag('cancer_dashboard/buttons/dashboard_button.html')
def dashboard_button(model_wrapper):
    subject_dashboard_url = settings.DASHBOARD_URL_NAMES.get(
        'subject_dashboard_url')
    return dict(
        subject_dashboard_url=subject_dashboard_url,
        subject_identifier=model_wrapper.subject_identifier)
