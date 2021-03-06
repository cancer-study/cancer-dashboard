import re

from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.utils.decorators import method_decorator
from edc_base.utils import get_utcnow
from edc_base.view_mixins import EdcBaseViewMixin
from edc_constants.constants import MALE
from edc_dashboard.view_mixins import ListboardFilterViewMixin, SearchFormViewMixin
from edc_dashboard.views import ListboardView
from edc_navbar import NavbarViewMixin

from ....model_wrappers import SubjectConsentModelWrapper
from .filters import ListboardViewFilters


class SubjectConsentListboardView(NavbarViewMixin, EdcBaseViewMixin,
                                  ListboardFilterViewMixin, SearchFormViewMixin,
                                  ListboardView):

    listboard_template = 'subject_listboard_template'
    listboard_url = 'subject_listboard_url'
    listboard_panel_style = 'success'
    listboard_fa_icon = "far fa-user-circle"

    listboard_view_filters = ListboardViewFilters()
    model = 'cancer_subject.subjectconsent'
    model_wrapper_cls = SubjectConsentModelWrapper
    app_config_name = 'cancer_dashboard'
    navbar_name = 'cancer_dashboard'
    navbar_selected_item = 'consented_subject'
    ordering = '-modified'
    paginate_by = 10
    search_form_url = 'subject_listboard_url'

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(
            MALE=MALE,
            subject_consent_add_url=self.model_cls().get_absolute_url(),
            reference_datetime=get_utcnow())
        return context

    def get_queryset_filter_options(self, request, *args, **kwargs):
        options = super().get_queryset_filter_options(request, *args, **kwargs)
        try:
            options.pop('site')
        except KeyError:
            pass
        if kwargs.get('subject_identifier'):
            options.update(
                {'subject_identifier': kwargs.get('subject_identifier')})
        return options

    def extra_search_options(self, search_term):
        q = Q()
        if re.match('^[A-Z]+$', search_term):
            q = Q(first_name__exact=search_term)
        return q
