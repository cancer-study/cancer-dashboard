from django.apps import AppConfig as DjangoAppConfig
from django.conf import settings


class AppConfig(DjangoAppConfig):
    name = 'cancer_dashboard'

    admin_site_name = 'cancer_subject_admin'
    base_template_name = 'edc_base/base.html'
    dashboard_template_name = 'cancer_dashboard/subject/dashboard.html'
    dashboard_url_name = 'cancer_dashboard:subject_dashboard_url'

    listboard_template_name = 'cancer_dashboard/subject/listboard.html'
    listboard_url_name = 'cancer_dashboard:consent_listboard_url'

    screening_listboard_template_name = 'cancer_dashboard/screening/listboard.html'
    screening_listboard_url_name = 'cancer_dashboard:screening_listboard_url'


if settings.APP_NAME == 'cancer_dashboard':

    from edc_appointment.appointment_config import AppointmentConfig
    from edc_appointment.apps import AppConfig as BaseEdcAppointmentAppConfig
    from edc_facility.apps import AppConfig as BaseEdcFacilityAppConfig
    from dateutil.relativedelta import MO, TU, WE, TH, FR, SA, SU

    class EdcAppointmentAppConfig(BaseEdcAppointmentAppConfig):
        configurations = [
            AppointmentConfig(
                model='edc_appointment.appointment',
                related_visit_model='cancer_dashboard.subjectvisit',
                appt_type='hospital')]

    class EdcFacilityAppConfig(BaseEdcFacilityAppConfig):
        country = 'botswana'
        definitions = {
            '7-day clinic': dict(days=[MO, TU, WE, TH, FR, SA, SU],
                                 slots=[100, 100, 100, 100, 100, 100, 100]),
            '5-day clinic': dict(days=[MO, TU, WE, TH, FR],
                                 slots=[100, 100, 100, 100, 100])}