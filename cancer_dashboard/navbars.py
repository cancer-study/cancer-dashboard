from django.conf import settings
from edc_navbar import NavbarItem, site_navbars, Navbar


no_url_namespace = True if settings.APP_NAME == 'cancer_dashboard' else False

cancer_dashboard = Navbar(name='cancer_dashboard')

cancer_dashboard.append_item(
    NavbarItem(
        name='screened_subject',
        title='Screening',
        label='screening',
        fa_icon='fa fa-user-plus',
        url_name=settings.DASHBOARD_URL_NAMES['screening_listboard_url'],
        no_url_namespace=no_url_namespace))

cancer_dashboard.append_item(
    NavbarItem(
        name='consented_subject',
        title='Subjects',
        label='subjects',
        fa_icon='far fa-user-circle',
        url_name=settings.DASHBOARD_URL_NAMES['subject_listboard_url'],
        no_url_namespace=no_url_namespace))

site_navbars.register(cancer_dashboard)
