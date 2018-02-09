from django.conf import settings

if settings.APP_NAME == 'cancer_dashboard':
    from .tests import models
