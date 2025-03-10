import pytz
from django.apps import apps as django_apps
from django.core.exceptions import ObjectDoesNotExist
from django.views.generic.base import ContextMixin
from edc_action_item.site_action_items import site_action_items
from edc_base.view_mixins import EdcBaseViewMixin
from edc_base.utils import get_utcnow
from edc_constants.constants import OFF_STUDY, YES, NEW
from edc_dashboard.views import DashboardView as BaseDashboardView
from edc_navbar import NavbarViewMixin
from edc_subject_dashboard.view_mixins import SubjectDashboardViewMixin
from edc_visit_schedule.site_visit_schedules import site_visit_schedules

from cancer_prn.action_items import DEATH_REPORT_ACTION, SUBJECT_OFFSTUDY_ACTION
from cancer_subject.action_items import SUBJECT_LOCATOR_ACTION
from ....model_wrappers import (
    SubjectVisitModelWrapper, SubjectConsentModelWrapper,
    SubjectScreeningModelWrapper, AppointmentModelWrapper,
    SubjectLocatorModelWrapper)

tz = pytz.timezone('Africa/Gaborone')


class AddSubjectScreening(ContextMixin):

    @property
    def subject_screening_model_obj(self):
        """Returns a subject screening model instance or None.
        """
        try:
            return self.subject_screening_cls.objects.get(
                **self.subject_screening_options)
        except ObjectDoesNotExist:
            return None

    @property
    def subject_screening(self):
        """Returns a wrapped saved or unsaved subject screening.
        """
        model_obj = self.subject_screening_model_obj or self.subject_screening_cls(
            **self.create_subject_screening_options)
        return SubjectScreeningModelWrapper(model_obj=model_obj)

    @property
    def subject_screening_cls(self):
        return django_apps.get_model('cancer_subject.subjectscreening')

    @property
    def create_subject_screening_options(self):
        """Returns a dictionary of options to create a new
        unpersisted cancer subject model instance.
        """
        options = dict(
            subject_identifier=self.subject_identifier)
        return options

    @property
    def subject_screening_options(self):
        """Returns a dictionary of options to get an existing
        subject screening model instance.
        """
        options = dict(
            subject_identifier=self.subject_identifier)
        return options

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(subject_screening=self.subject_screening)
        return context


class DashboardView(
        AddSubjectScreening, EdcBaseViewMixin,
        SubjectDashboardViewMixin, NavbarViewMixin,
        BaseDashboardView):

    dashboard_url = 'subject_dashboard_url'
    dashboard_template = 'subject_dashboard_template'
    appointment_model = 'cancer_subject.appointment'
    appointment_model_wrapper_cls = AppointmentModelWrapper
    consent_model = 'cancer_subject.subjectconsent'
    consent_model_wrapper_cls = SubjectConsentModelWrapper
    navbar_name = 'cancer_dashboard'
    navbar_selected_item = 'consented_subject'
    subject_locator_model = 'cancer_subject.subjectlocator'
    subject_locator_model_wrapper_cls = SubjectLocatorModelWrapper
    visit_model_wrapper_cls = SubjectVisitModelWrapper
    special_forms_include_value = 'cancer_dashboard/subject/dashboard/special_forms.html'
    data_action_item_template = 'cancer_dashboard/subject/dashboard/data_manager.html'
    ssh_model = 'edc_visit_schedule.subjectschedulehistory'

    @property
    def ssh_model_cls(self):
        return django_apps.get_model(self.ssh_model)

    @property
    def appointments(self):
        """Returns a Queryset of all appointments for this subject.
        """
        if not self._appointments:
            self._appointments = self.appointment_model_cls.objects.filter(
                subject_identifier=self.subject_identifier).order_by(
                    'visit_code')
        return self._appointments

    def get_context_data(self, **kwargs):
        if ('switch' in self.request.path and
                'schedule_6months' not in self.current_schedule_names):
            self.switch_to_6months_schedule()

        context = super().get_context_data(**kwargs)
        self.get_subject_death_or_message()
        self.get_subject_offstudy_or_message()
        locator_obj = self.get_locator_info()
        context.update(
            YES=YES,
            locator_obj=locator_obj,
            current_schedule_names=self.current_schedule_names,
            enrolment_duration=self.get_enrolment_duration)
        return context

    def set_current_schedule(self, onschedule_model_obj=None,
                             schedule=None, visit_schedule=None,
                             is_onschedule=True):
        if onschedule_model_obj:
            self.current_schedule = schedule
            self.current_visit_schedule = visit_schedule
            self.current_onschedule_model = onschedule_model_obj
            self.onschedule_models.append(onschedule_model_obj)
            self.visit_schedules.update(
                {visit_schedule.name: visit_schedule})

    def get_onschedule_model_obj(self, schedule):
        try:
            return schedule.onschedule_model_cls.objects.get(
                subject_identifier=self.subject_identifier)
        except ObjectDoesNotExist:
            return None

    @property
    def current_schedule_names(self):
        subject_identifier = self.kwargs.get('subject_identifier')

        names = self.ssh_model_cls.objects.filter(
            subject_identifier=subject_identifier).values_list(
                'schedule_name', flat=True)
        return names

    @property
    def get_enrolment_duration(self):
        onschedule_model_cls = django_apps.get_model(
            'cancer_subject.onschedule')
        subject_identifier = self.kwargs.get('subject_identifier')
        try:
            onschedule_obj = onschedule_model_cls.objects.get(
                subject_identifier=subject_identifier)
        except onschedule_model_cls.DoesNotExist:
            return None
        else:
            onschedule_dt = onschedule_obj.onschedule_datetime
            return (get_utcnow() - onschedule_dt).days / 365

    def switch_to_6months_schedule(self):
        subject_identifier = self.kwargs.get('subject_identifier')
        try:
            ssh = self.ssh_model_cls.objects.get(
                subject_identifier=subject_identifier,
                schedule_name='schedule')
        except self.ssh_model_cls.DoesNotExist:
            return
        else:
            if ssh.schedule_status == 'onschedule':
                onschedule_dt = ssh.onschedule_datetime.astimezone(tz)
            remaining_appts = self.appointment_model_cls.objects.filter(
                subject_identifier=subject_identifier,
                appt_status='new')
            if remaining_appts.exists():
                _, schedule = site_visit_schedules.get_by_onschedule_model_schedule_name(
                    onschedule_model='cancer_subject.onschedule6months',
                    name='schedule_6months')
                schedule.put_on_schedule(
                    subject_identifier=subject_identifier,
                    onschedule_datetime=onschedule_dt)
                remaining_appts = self.appointment_model_cls.objects.filter(
                    subject_identifier=subject_identifier,
                    schedule_name='schedule',
                    appt_status='new')
                new_appts = self.appointment_model_cls.objects.filter(
                    subject_identifier=subject_identifier,
                    schedule_name='schedule_6months').exclude(
                    visit_code__in=remaining_appts.values_list('visit_code', flat=True))
                if new_appts:
                    new_appts.delete()
                remaining_appts.delete()

    def get_locator_info(self):

        subject_identifier = self.kwargs.get('subject_identifier')
        try:
            obj = self.subject_locator_model_cls.objects.get(
                subject_identifier=subject_identifier)
        except ObjectDoesNotExist:
            return None
        return obj

    def get_subject_locator_or_message(self):
        obj = self.get_locator_info()
        subject_identifier = self.kwargs.get('subject_identifier')

        if not obj:
            action_cls = site_action_items.get(
                self.subject_locator_model_cls.action_name)
            action_item_model_cls = action_cls.action_item_model_cls()
            try:
                action_item_model_cls.objects.get(
                    subject_identifier=subject_identifier,
                    action_type__name=SUBJECT_LOCATOR_ACTION)
            except ObjectDoesNotExist:
                action_cls(
                    subject_identifier=subject_identifier)
        return obj

    def get_subject_death_or_message(self):
        subject_visit_cls = django_apps.get_model(
            'cancer_subject.subjectvisit')
        subject_death_cls = django_apps.get_model(
            'cancer_prn.deathreport')
        subject_identifier = self.kwargs.get('subject_identifier')

        try:
            subject_visit_cls.objects.get(
                appointment__subject_identifier=subject_identifier,
                reason='Death')
        except ObjectDoesNotExist:
            self.delete_action_item_if_new(subject_death_cls)
        else:
            self.action_cls_item_creator(
                subject_identifier=subject_identifier,
                action_cls=subject_death_cls,
                action_type=DEATH_REPORT_ACTION)

    def get_subject_offstudy_or_message(self):
        subject_visit_cls = django_apps.get_model(
            'cancer_subject.subjectvisit')
        subject_offstudy_cls = django_apps.get_model(
            'cancer_prn.subjectoffstudy')
        LOST_TO_FOLLOWUP = 'Lost to follow-up'

        subject_identifier = self.kwargs.get('subject_identifier')
        off_study_reasons = [OFF_STUDY, LOST_TO_FOLLOWUP]
        obj = subject_visit_cls.objects.filter(
            reason__in=off_study_reasons,
            appointment__subject_identifier=subject_identifier)
        if not obj:
            self.delete_action_item_if_new(subject_offstudy_cls)
        if obj:
            self.action_cls_item_creator(
                subject_identifier=subject_identifier,
                action_cls=subject_offstudy_cls,
                action_type=SUBJECT_OFFSTUDY_ACTION)
        return obj

    def action_cls_item_creator(
            self, subject_identifier=None, action_cls=None, action_type=None):
        action_cls = site_action_items.get(
            action_cls.action_name)
        action_item_model_cls = action_cls.action_item_model_cls()
        try:
            action_item_model_cls.objects.get(
                subject_identifier=subject_identifier,
                action_type__name=action_type)
        except ObjectDoesNotExist:
            action_cls(
                subject_identifier=subject_identifier)

    def delete_action_item_if_new(self, action_model_cls):
        action_item_obj = self.get_action_item_obj(action_model_cls)
        if action_item_obj:
            action_item_obj.delete()

    def get_action_item_obj(self, model_cls):
        subject_identifier = self.kwargs.get('subject_identifier')
        action_cls = site_action_items.get(
            model_cls.action_name)
        action_item_model_cls = action_cls.action_item_model_cls()

        try:
            action_item_obj = action_item_model_cls.objects.get(
                subject_identifier=subject_identifier,
                action_type__name=model_cls.action_name,
                status=NEW)
        except action_item_model_cls.DoesNotExist:
            return None
        return action_item_obj
