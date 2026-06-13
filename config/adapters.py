import logging

from allauth.account.adapter import DefaultAccountAdapter
from django.contrib import messages

logger = logging.getLogger(__name__)


class CustomAccountAdapter(DefaultAccountAdapter):
    """Prevent SMTP failures from blocking signup/login flows."""

    def send_mail(self, template_prefix, email, context):
        try:
            return super().send_mail(template_prefix, email, context)
        except Exception as exc:
            logger.warning("Email send failed (%s → %s): %s", template_prefix, email, exc)
            return None

    def add_message(self, request, level, message_template, message_context=None, extra_tags=""):
        try:
            super().add_message(request, level, message_template, message_context, extra_tags)
        except Exception:
            if level >= messages.ERROR:
                messages.error(request, "An error occurred. Please try again.")
