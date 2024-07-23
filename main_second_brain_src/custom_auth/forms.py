from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser, InvitationKey


class CustomUserCreationForm(UserCreationForm):
    """
    A form for creating new users, extending the default UserCreationForm.

    This form includes an additional field for an invitation key.

    Meta:
        model (CustomUser): The model that this form is linked to.
        fields (tuple): The fields to be included in the form.
    """
    invitation_key = forms.CharField(max_length=50)

    class Meta:
        model = CustomUser
        fields = ('username', 'firstname', 'lastname', 'email',
                  'phonenumber', 'date_of_birth', 'role', 'invitation_key')

    def clean_invitation_key(self):
        """
        Validate the invitation key.

        This method checks if the provided invitation key exists and is not already used.
        If the key is invalid or already used, a ValidationError is raised.

        Returns:
            key(str): The cleaned invitation key.

        Raises:
            forms.ValidationError: If the invitation key is invalid or already used.
        """
        key = self.cleaned_data.get('invitation_key')
        try:
            invitation = InvitationKey.objects.get(key=key, is_used=False)
        except InvitationKey.DoesNotExist:
            raise forms.ValidationError(
                'Invalid or already used invitation key.')
        return key

    def save(self, commit=True):
        """
        Save the new user and mark the invitation key as used.

        This method saves the user instance and updates the invitation key status to used.

        Args:
            commit (bool): Whether to commit the save operation immediately.

        Returns:
            CustomUser: The saved user instance.
        """
        user = super().save(commit=False)
        invitation_key = self.cleaned_data.get('invitation_key')
        invitation = InvitationKey.objects.get(key=invitation_key)
        if not invitation.is_forever:
            invitation.is_used = True
            invitation.save()

        if commit:
            user.save()
        return user
