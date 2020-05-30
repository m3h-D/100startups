from django import forms
from django.contrib.auth.forms import ReadOnlyPasswordHashField, SetPasswordForm
from django.contrib.auth import authenticate
from .models import User, Role
from startup.models import UserProfile


class UserStartupRegisterForm(forms.ModelForm):
    """a custom form for admin.py
    
    Arguments:
        forms {MODULE} -- a django built-in ModelForm
    
    Raises:
        forms.ValidationError: raise an error if passowrds don't match
    
    Returns:
        OBJECT -- returns created user
    """
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(
        label='Password confirmation', widget=forms.PasswordInput)

    class Meta:
        models = User
        fields = ('phone', 'email',)

    def clean_password2(self):
        """check if the passwords match
        
        Raises:
            forms.ValidationError: raise an error if passwords are not match
        
        Returns:
            STRING -- returns password2
        """
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        """set user passowrd before saving to database
        
        Keyword Arguments:
            commit {BOOLEAN} -- to stop commit when setting password (default: {True})
        
        Returns:
            OBJECT -- returns created user
        """
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class UserChangeForm(forms.ModelForm):
    """A form for updating users. Includes all the fields on
    the user, but replaces the password field with admin's
    password hash display field.
    """
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = User
        fields = ('email', 'phone', 'password', 'is_active', 'is_admin')

    def clean_password(self):
        return self.initial["password"]




class UserProfileForm(forms.ModelForm):
    """a form for startups owner to fill additional information
    
    Arguments:
        forms {MODULE} -- a django built-in Model Form
    """
    class Meta:
        models = UserProfile
        exclude = ('user',)



class UserRegisterForm(forms.ModelForm):
    """a form for user to fill additional information
    
    Arguments:
        forms {MODULE} -- a django built-in Model Form
    """
    class Meta:
        model = User
        fields = ('phone',)


class UserCreateRole(forms.ModelForm):
    """a form to create karmand type user
    
    Arguments:
        forms {MODULE} -- a django built-in Model Form
    """
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'phone', 'email')


class LeaderForm(forms.ModelForm):
    """a form for startups owner to fill additional information
    
    Arguments:
        forms {MODULE} -- a django built-in Model Form
    """
    class Meta:
        model = UserProfile
        fields = ('saham', 'duration_per_month')


class LeaderUserForm(forms.ModelForm):
    """a form for user to fill additional information
    
    Arguments:
        forms {MODULE} -- a django built-in Model Form
    """
    class Meta:
        model = User
        fields = ('phone', 'first_name', 'last_name',
                  'email', 'linkdin', 'grade', 'skill')



class KarmandForm(forms.ModelForm):
    """a form to create karmand type user
    
    Arguments:
        forms {MODULE} -- a django built-in Model Form
    """
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username',
                  'phone', 'email', 'linkdin', 'multi', 'avatar', 'can_see_startups')


class ProfileAdminForm(forms.ModelForm):
    """a form for user to fill additional information
    
    Arguments:
        forms {MODULE} -- a django built-in Model Form
    """
    class Meta:
        model = User
        fields = ('email', 'linkdin', 'skill', 'grade')


class ProfileRoleForm(forms.ModelForm):
    """a form for user to fill additional information
    
    Arguments:
        forms {MODULE} -- a django built-in Model Form
    """
    class Meta:
        model = User
        fields = ('email', 'linkdin', 'twitter', 'site',
                  'city', 'instagram', 'bio', 'skill', 'grade')


class PasswordChangeForm(SetPasswordForm):
    """
    A form that lets a user change their password by entering their old
    password.
    """
    error_messages = {
        **SetPasswordForm.error_messages,
    }

    field_order = ['new_password1', 'new_password2']





class LoginForm(forms.Form):
    """a custom form for login
    
    Arguments:
        forms {MODULE} -- a django built-in Model Form
    """
    username = forms.CharField(max_length=120)
    password = forms.CharField(
        max_length=120, widget=forms.PasswordInput)