from django.contrib.auth import get_user_model

User = get_user_model()

class MyAuthBackend:
    def authenticate(self, request, email=None, password=None):
        if email is None or password is None:
            # nothing to do
            return None

        # get 'TblUsers' object
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return None

        # authenticate user
        if not password == user.password:
            return None

        return user

    def get_user(self, pk):
        try:
            return User.objects.get(pk=pk)
        except User.DoesNotExist:
            pass

        return None
