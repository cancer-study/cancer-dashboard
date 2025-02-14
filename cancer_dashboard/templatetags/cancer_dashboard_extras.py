from urllib.parse import urlencode, unquote

from django import template
from django.conf import settings
from django.utils.safestring import mark_safe

from edc_appointment.constants import NEW_APPT, INCOMPLETE_APPT, COMPLETE_APPT, \
    IN_PROGRESS_APPT
from edc_visit_schedule.models import SubjectScheduleHistory

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


@register.inclusion_tag('cancer_dashboard/buttons/appointment_button.html')
def appointment_button(model_wrapper):
    if hasattr(model_wrapper, 'disabled'):
        title = 'Start, continue or restart data collection for this timepoint.'
    else:
        title = 'Disabled while another appointment is in progress.'
    return dict(
        title=title,
        wrapped=model_wrapper,
        NEW_APPT=NEW_APPT,
        IN_PROGRESS_APPT=IN_PROGRESS_APPT,
        INCOMPLETE_APPT=INCOMPLETE_APPT,
        COMPLETE_APPT=COMPLETE_APPT,
    )


@register.inclusion_tag('cancer_dashboard/subject_schedule_footer_row.html')
def subject_schedule_footer_row(subject_identifier, visit_schedule, schedule,
                                subject_dashboard_url):

    context = {}
    try:
        history_obj = SubjectScheduleHistory.objects.get(
            visit_schedule_name=visit_schedule.name,
            schedule_name=schedule.name,
            subject_identifier=subject_identifier,
            offschedule_datetime__isnull=False)
    except SubjectScheduleHistory.DoesNotExist:
        onschedule_model_obj = schedule.onschedule_model_cls.objects.get(
            subject_identifier=subject_identifier, )
        options = dict(subject_identifier=subject_identifier)
        query = unquote(urlencode(options))
        href = (f'{visit_schedule.offstudy_model_cls().get_absolute_url()}?next='
                f'{subject_dashboard_url},subject_identifier')
        href = '&'.join([href, query])
        context = dict(
            offschedule_datetime=None,
            onschedule_datetime=onschedule_model_obj.onschedule_datetime,
            href=mark_safe(href))
    else:
        onschedule_model_obj = schedule.onschedule_model_cls.objects.get(
            subject_identifier=subject_identifier, )
        options = dict(subject_identifier=subject_identifier)
        query = unquote(urlencode(options))
        offstudy_model_obj = None
        try:
            offstudy_model_obj = visit_schedule.offstudy_model_cls.objects.get(
                subject_identifier=subject_identifier)
        except visit_schedule.offstudy_model_cls.DoesNotExist:
            href = (f'{visit_schedule.offstudy_model_cls().get_absolute_url()}'
                    f'?next={subject_dashboard_url},subject_identifier')
        else:
            href = (f'{offstudy_model_obj.get_absolute_url()}?next='
                    f'{subject_dashboard_url},subject_identifier')

        href = '&'.join([href, query])

        context = dict(
            offschedule_datetime=history_obj.offschedule_datetime,
            onschedule_datetime=onschedule_model_obj.onschedule_datetime,
            href=mark_safe(href))
        if offstudy_model_obj:
            context.update(offstudy_date=offstudy_model_obj.offstudy_date)
    context.update(
        visit_schedule=visit_schedule,
        schedule=schedule,
        verbose_name=visit_schedule.offstudy_model_cls._meta.verbose_name)
    return context
