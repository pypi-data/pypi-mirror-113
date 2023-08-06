from django.conf import settings
from django.http import HttpResponseRedirect
from django.urls import resolve, reverse
from django.urls.exceptions import NoReverseMatch

AUTH_SETTINGS = getattr(settings, "AUTH_SETTINGS", {})
LOGIN_URL = AUTH_SETTINGS.get("LOGIN_URL", "login")
DEFAULT_REDIRECT = AUTH_SETTINGS.get("DEFAULT_REDIRECT", None)
LOCK_URLS = AUTH_SETTINGS.get("LOCK_URLS", set())


class AuthRequiredMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        assert isinstance(LOCK_URLS, set), 'LOCK_URLS must be of type "set".'

        if len(LOCK_URLS) == 0:
            return self.get_response(request)

        try:
            current_url = resolve(request.path_info).url_name
            if current_url in LOCK_URLS and not request.user.is_authenticated:
                return HttpResponseRedirect(
                    reverse(LOGIN_URL) + "?next=" + request.path
                )

            if request.user.is_authenticated and current_url in LOGIN_URL:
                if DEFAULT_REDIRECT:
                    return HttpResponseRedirect(reverse(DEFAULT_REDIRECT))

        except NoReverseMatch:
            if DEFAULT_REDIRECT:
                return HttpResponseRedirect(reverse(DEFAULT_REDIRECT))

        return self.get_response(request)
