from two_factor.views import LoginView as TwoFactorLoginView
from two_factor.forms import AuthenticationTokenForm, BackupTokenForm
from email_from_template import send_mail

from django.conf import settings
from django.urls import reverse_lazy
from django.contrib import auth, messages
from django.shortcuts import redirect
from django.contrib.auth import get_user_model, views as auth_views

from freenodejobs.utils import log
from freenodejobs.utils.ratelimit import rate_limit

from .forms import AuthenticationForm

UserModel = get_user_model()


class LoginView(TwoFactorLoginView):
    template_name = 'account/login.html'
    form_list = (
        ('auth', AuthenticationForm),
        ('token', AuthenticationTokenForm),
        ('backup', BackupTokenForm),
    )

    def dispatch(self, request):
        if request.user.is_authenticated:
            if request.user.is_staff:
                return redirect('admin:view')
            return redirect(settings.LOGIN_REDIRECT_URL)

        return super().dispatch(request)

    def done(self, *args, **kwargs):
        response = super().done(*args, **kwargs)

        log.info(self.request, "Login successful")

        if self.request.user.is_staff and \
                self.redirect_field_name not in self.request.GET:
            return redirect('admin:view')

        return response

    def render(self, *args, **kwargs):
        if self.request.method == 'POST' and self.steps.current == 'auth':
            self.invalid_auth()

        return super().render(*args, **kwargs)

    def invalid_auth(self):
        num = 3
        minutes = 5
        seconds = 60 * minutes

        email = self.request.POST.get('auth-email', '')
        ip_address = self.request.META['REMOTE_ADDR']

        log.warning(self.request, "Rejected login attempt for {!r}".format(
                    email))

        for resource, val, prefix in (
            ('login:email', email, "for the email"),
            ('login:ip', ip_address, "from IP address"),
        ):
            if not val:
                continue

            # We have not reached a trigger limit
            if not rate_limit(resource, val, num - 1, seconds):
                continue

            # Avoid sending multiple emails
            if rate_limit('login:alert', None, 1, seconds):
                break

            staff = UserModel.objects.filter(is_staff=True) \
                .values_list('email', flat=True)

            send_mail((), 'account/alert.email', {
                'val': val,
                'num': num,
                'prefix': prefix,
                'minutes': minutes,
            }, bcc=staff, fail_silently=True)


def logout(request):
    auth.logout(request)

    messages.success(request, "You have been successfully Logged out.")

    return redirect(settings.LOGOUT_REDIRECT_URL)


class PasswordChangeView(auth_views.PasswordChangeView):
    success_url = reverse_lazy('account:password-change')
    template_name = 'account/password_change.html'

    def form_valid(self, form):
        super().form_valid(form)

        messages.success(self.request,
                         "Your password has been changed successfully.")

        return redirect('account:password-change')
