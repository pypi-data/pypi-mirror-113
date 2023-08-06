from django.conf import settings
from django.http import HttpResponseRedirect
from django.shortcuts import redirect
from django.urls import resolve, reverse
from django.utils.deprecation import MiddlewareMixin

AUTH_SETTINGS = getattr(settings, "AUTH_SETTINGS", {})
LOGIN_URL = AUTH_SETTINGS.get("LOGIN_URL", None)
LOGOUT_URL = AUTH_SETTINGS.get("LOGOUT_URL", None)
DEFAULT_REDIRECT = AUTH_SETTINGS.get("DEFAULT_REDIRECT", None)
LOCK_URLS = AUTH_SETTINGS.get("LOCK_URLS", None)


class AuthRequiredMiddleware(MiddlewareMixin):
    def __init__(self, get_response):
        self.get_response = get_response

    def process_request(self, request):
        assert hasattr(request, "user")
        current_url = resolve(request.path_info).url_name

        if current_url == DEFAULT_REDIRECT or current_url == LOGIN_URL:
            return None

        if not request.user.is_authenticated:
            if current_url in LOCK_URLS:
                return HttpResponseRedirect(
                    reverse(LOGIN_URL) + "?next=" + request.path
                )

            # Fail-safe redirect
            return redirect(DEFAULT_REDIRECT)

        if request.user.is_authenticated and current_url in LOGIN_URL:
            return redirect(DEFAULT_REDIRECT)

        return None
