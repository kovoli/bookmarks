from django.db import models
from django.conf import settings


class Profile(models.Model):
    """
    Поле user «один к одному» позволяет вам связывать профили с пользователями. 
    Мы используем CASCADE для параметра  on_delete , чтобы связанный с ним профиль
    также удалялся при удалении пользователя.
    """
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    date_of_birth = models.DateField(blank=True, null=True)
    photo = models.ImageField(upload_to='users/%Y/%m/%d/', blank=True)

    def __str__(self):
        return 'Profile for user {}'.format(self.user.username)



