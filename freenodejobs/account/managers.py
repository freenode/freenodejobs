from django.contrib.auth.models import BaseUserManager


class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, email, password, **kwargs):
        email = self.normalize_email(email)
        user = self.model(email=email, **kwargs)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **kwargs):
        kwargs['is_staff'] = False
        kwargs['is_superuser'] = False
        return self._create_user(email, password, **kwargs)

    def create_staff(self, email, password=None, **kwargs):
        kwargs['is_staff'] = True
        kwargs['is_superuser'] = False
        return self._create_user(email, password, **kwargs)

    def create_superuser(self, email, password, **kwargs):  # pragma: no-cover
        kwargs['is_staff'] = True
        kwargs['is_superuser'] = True
        return self._create_user(email, password, **kwargs)
