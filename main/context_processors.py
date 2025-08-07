from django.conf import settings


def settings_context(request):
    """
    Context processor that injects Django settings into all templates.
    
    This makes all settings available in templates, allowing for dynamic
    configuration display and debugging.
    """
    return {
        'settings': settings,
        'DEBUG': settings.DEBUG,
        'ALLOWED_HOSTS': settings.ALLOWED_HOSTS,
        'DATABASES': settings.DATABASES,
        'INSTALLED_APPS': settings.INSTALLED_APPS,
        'MIDDLEWARE': settings.MIDDLEWARE,
        'ROOT_URLCONF': settings.ROOT_URLCONF,
        'TEMPLATES': settings.TEMPLATES,
        'WSGI_APPLICATION': settings.WSGI_APPLICATION,
        'SECRET_KEY': settings.SECRET_KEY[:10] + '...' if len(settings.SECRET_KEY) > 10 else settings.SECRET_KEY,
        'STATIC_URL': settings.STATIC_URL,
        'MEDIA_URL': getattr(settings, 'MEDIA_URL', ''),
        'LANGUAGE_CODE': settings.LANGUAGE_CODE,
        'TIME_ZONE': settings.TIME_ZONE,
        'USE_I18N': settings.USE_I18N,
        'USE_TZ': settings.USE_TZ,
        'DEFAULT_AUTO_FIELD': settings.DEFAULT_AUTO_FIELD,
    } 