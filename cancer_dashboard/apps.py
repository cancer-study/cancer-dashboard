from django.apps import AppConfig as DjangoAppConfig


class AppConfig(DjangoAppConfig):
    name = 'cancer_dashboard'

    admin_site_name = 'cancer_subject_admin'
    base_template_name = 'edc_base/base.html'
    dashboard_template_name = 'cancer_dashboard/subject/dashboard.html'
    dashboard_url_name = 'cancer_dashboard:dashboard_url'

    listboard_template_name = 'cancer_dashboard/subject/listboard.html'
    listboard_url_name = 'cancer_dashboard:consent_listboard_url'

    checklist_listboard_template_name = 'cancer_dashboard/checklist/listboard.html'
    checklist_listboard_url_name = 'cancer_dashboard:checklist_listboard_url'
