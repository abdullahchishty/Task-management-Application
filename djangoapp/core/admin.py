from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User,UserMessage,EmailComposition
# from .forms import EmailComposeForm
from . import views
from django.urls import path
from .models import EmailComposition
from django.core.mail import send_mail
from django.conf import settings
# from objectactions import act, BaseAdmin


#admin can handle user through this decorator
@admin.register(User)
class UserAdmin(BaseUserAdmin):
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'password1', 'password2', 'email', 'first_name', 'last_name','phone','bio','interest','image'),
        }),
    )

admin.site.register(UserMessage)

from django.core.mail import send_mail

def send_email_action(modeladmin, request, queryset):
    for email_composition in queryset:
        subject = email_composition.subject
        message = email_composition.message_content
        from_email = settings.EMAIL_HOST_USER
        recipients = [user.email for user in email_composition.recipients.all()]
        send_mail(subject, message, from_email, recipients)
        email_composition.sent = True
        email_composition.save()

send_email_action.short_description = "Send Email to Selected Compositions"

@admin.register(EmailComposition)
class EmailCompositionAdmin(admin.ModelAdmin):
    list_display = ['subject', 'recipients_list']
    actions = ['send_email_action']

    def recipients_list(self, obj):
        return ", ".join([str(user) for user in obj.recipients.all()])
    recipients_list.short_description = "Recipients"








