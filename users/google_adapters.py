from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from budget.models import Users


class GoogleAccountAdapter(DefaultSocialAccountAdapter):
    
    def pre_social_login(self, request, sociallogin):
        """
        Link Google account to existing user with same email
        """
        if sociallogin.is_existing:
            return

        email = sociallogin.account.extra_data.get("email")
        
        try:
            user = Users.objects.get(email=email)
            sociallogin.connect(request, user)
            
        except Users.DoesNotExist:
            pass
    
    def save_user(self, request, sociallogin, form=None):
        user = super().save_user(request, sociallogin, form)

        user.name = sociallogin.account.extra_data.get('name')
        user.is_staff = True
        user.save()

        return user