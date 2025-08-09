from allauth.account.adapter import DefaultAccountAdapter
from allauth.account.models import EmailConfirmation
from allauth.account.models import EmailAddress
from allauth.account.utils import user_email
from django.conf import settings
from django.utils import timezone


class CustomAccountAdapter(DefaultAccountAdapter):
    def send_confirmation_mail(self, request, emailconfirmation, signup):

        user = emailconfirmation.email_address.user

        email = user_email(user)
        email_address, _ = EmailAddress.objects.get_or_create(
            user=user,
            email=email,
            defaults={'verified': False, 'primary': True}
        )

        confirmation = EmailConfirmation.create(email_address)
        confirmation.key = emailconfirmation.key
        confirmation.sent = timezone.now()
        confirmation.save()

        ctx = {
            "user": emailconfirmation.email_address.user,
        }
        if settings.ACCOUNT_EMAIL_VERIFICATION_BY_CODE_ENABLED:
            ctx.update({"code": emailconfirmation.key})
        else:
            ctx.update(
                {
                    "key": emailconfirmation.key,
                    "activate_url": self.get_email_confirmation_url(
                        request, emailconfirmation
                    ),
                }
            )
        if signup:
            email_template = "account/email/email_confirmation_signup"
        else:
            email_template = "account/email/email_confirmation"
        self.send_mail(email_template, emailconfirmation.email_address.email, ctx)

    def send_password_reset_mail(self, user, email, context):
        """
        Method intended to be overridden in case you need to customize the logic
        used to determine whether a user is permitted to request a password reset.
        For example, if you are enforcing something like "social only" authentication
        in your app, you may want to intervene here by checking `user.has_usable_password`

        """
        ctx = {
            "user": user,
            "password_reset_url": "https://example.com/reset",
        }
        context.update(ctx)
        return self.send_mail("account/email/password_reset_key", email, context)
