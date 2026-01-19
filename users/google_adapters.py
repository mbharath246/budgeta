from allauth.socialaccount.adapter import DefaultSocialAccountAdapter



class GoogleAccountAdapter(DefaultSocialAccountAdapter):
    
    def save_user(self, request, sociallogin, form=None):
        user = super().save_user(request, sociallogin, form)

        user.name = sociallogin.account.extra_data.get('name')
        user.is_staff = True
        user.save()

        return user