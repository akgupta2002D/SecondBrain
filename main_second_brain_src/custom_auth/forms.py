from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser, InvitationKey


class CustomUserCreationForm(UserCreationForm):
    invitation_key = forms.CharField(max_length=50)

    class Meta:
        model = CustomUser
        fields = ('username', 'firstname', 'lastname', 'email',
                  'phonenumber', 'date_of_birth', 'role', 'invitation_key')

    def clean_invitation_key(self):
        key = self.cleaned_data.get('invitation_key')
        try:
            invitation = InvitationKey.objects.get(key=key, is_used=False)
        except InvitationKey.DoesNotExist:
            raise forms.ValidationError(
                'Invalid or already used invitation key.')
        return key

    def save(self, commit=True):
        user = super().save(commit=False)
        invitation_key = self.cleaned_data.get('invitation_key')
        invitation = InvitationKey.objects.get(key=invitation_key)
        invitation.is_used = True
        invitation.save()
        if commit:
            user.save()
        return user
