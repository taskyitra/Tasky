from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse_lazy
from django.utils import translation
from django.utils.functional import SimpleLazyObject
from user_account.models import UserProfile


class FrontendLanguageMiddleware(object):
    """
    Change the active language when visiting a frontend page.
    """
    def __init__(self):
        # NOTE: not locale aware, assuming the admin stays at a single URL.
        self._admin_prefix = reverse_lazy('admin:index', prefix='/')

    def process_request(self, request):
        # if request.path_info.startswith(str(self._admin_prefix)):
        #     return  # Excluding the admin

        # Проверка на ошибку локали
        if not hasattr(request, 'user'):
            return
        if str(request.user) == 'AnonymousUser':
            return
        user_locale = UserProfile.Locals[UserProfile.objects.get_or_create_profile(request.user).locale][1]
        if user_locale == 'en':
            request.LANGUAGE_CODE = 'en'
        if user_locale == 'ru':
            request.LANGUAGE_CODE = 'ru'
        translation.activate(user_locale)

