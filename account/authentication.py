from django.contrib.auth.models import User


class EmailAuthBackend:
    """
    логинг с помошью емайла

    - authenticate(): Он принимает объект request и учетные данные пользователя как параметры.
    Он должен вернуть объект user, который соответствует этим учетным данным, если учетные данные действительны,
    или None в противном случае. Параметр request является HttpRequest объектом, или None если он не предоставляется
    authenticate().
    - get_user(): Принимает параметр идентификатора пользователя и должен вернуть user объект.
    """
    def authenticate(self, request, username=None, password=None):
        try:
            user = User.objects.get(email=username)
            if user.check_password(password):
                return user
            return None
        except User.DoesNotExist:
            return None

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
