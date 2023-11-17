from django.contrib.auth.base_user import BaseUserManager, AbstractBaseUser
from django.db import models


class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, username, password, **extra_fields):
        """
        Create and save a user with the given username, email, and password.
        """
        if not username:
            raise ValueError('The given username must be set')
        user = self.model(email=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, username=None, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        extra_fields.setdefault('is_active', True)
        return self._create_user(username, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
        return self._create_user(email, password, **extra_fields)


class User(AbstractBaseUser):
    email = models.EmailField(
        verbose_name='Email',
        max_length=255,
        null=False,
        blank=False,
        unique=True
    )
    is_active = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField('Дата создания', auto_now_add=True)

    name = models.TextField(verbose_name="Имя", null=True, blank=False)

    last_change_password_attempt_datetime = models.DateTimeField(
        verbose_name="Дата и время последней попытки смены пароля",
        null=True,
        blank=True
    )

    password_recovery_token = models.CharField(max_length=255, null=True, blank=True)

    objects = UserManager()
    USERNAME_FIELD = 'email'

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        """Does the user have a specific permission?"""
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        """Does the user have permissions to view the app `app_label`?"""
        # Simplest possible answer: Yes, always
        return True


class SupplierBan(models.Model):
    supplier = models.ForeignKey(
        "Company",
        on_delete=models.CASCADE,
        related_name="bans",
        null=False,
        blank=False,
        verbose_name="Поставщик"
    )

    reason = models.TextField(null=False, blank=False, verbose_name="Причина")

    start_datetime = models.DateTimeField(null=False, blank=False, verbose_name="Дата и время начала блокировки")
    end_datetime = models.DateTimeField(null=False, blank=False, verbose_name="Дата и время окончания блокировки")

    ban_duration = models.DurationField(null=False, blank=False, verbose_name="Длительность блокировки")

    def save(
        self, force_insert=False, force_update=False, using=None, update_fields=None
    ):
        self.ban_duration = self.end_datetime - self.start_datetime
        super().save(force_insert, force_update, using, update_fields)


class Kpp(models.Model):
    kpp = models.CharField(max_length=9, null=True, blank=True, verbose_name="КПП")

    company = models.ForeignKey(
        "Company",
        on_delete=models.CASCADE,
        related_name="kpps",
        null=False,
        blank=False,
        verbose_name="Компания"
    )


class Company(models.Model):
    inn = models.CharField(max_length=12, null=False, blank=False, verbose_name="ИНН")

    is_supplier = models.BooleanField(verbose_name="Поставщик?", null=False, blank=False, default=False)
    is_contractor = models.BooleanField(verbose_name="Покупатель?", null=False, blank=False, default=False)

    class Meta:
        verbose_name = "Компания"
        verbose_name_plural = "Компании"


class QuotationSession(models.Model):
    # Participant_inn, Participant_kpp
    supplier = models.ForeignKey(
        "Company",
        on_delete=models.SET_NULL,
        related_name="participation",
        null=True,
        blank=False,
        verbose_name=""
    )

    # Is_winner
    is_winner = models.BooleanField(null=True, blank=True, verbose_name="Победитель?")

    # Id_ks
    external_id = models.IntegerField(primary_key=True, unique=True, verbose_name="ID")

    # Publish_date
    date_created = models.DateTimeField(null=False, blank=False, verbose_name="Дата публикации")

    price = models.FloatField(null=False, blank=False, verbose_name="Начальная максимальная цена")

    tender = models.ForeignKey(
        "Tender",
        on_delete=models.CASCADE,
        related_name="quotation_sessions",
        null=False,
        blank=False,
        verbose_name="Тендер"
    )

    violations = models.BooleanField(
        null=False,
        blank=False,
        default=False,
        verbose_name="Наличие нарушений по сроку подписания протокола котировочной сессии"
    )


class Region(models.Model):
    name = models.CharField(max_length=255, null=False, blank=False, verbose_name="Название")
    code = models.CharField(
        max_length=255,
        null=False,
        blank=False,
        verbose_name="Код региона",
        primary_key=True,
        unique=True
    )

    class Meta:
        verbose_name = "Регион"
        verbose_name_plural = "Регионы"

    def __str__(self):
        return f"{self.code}: {self.name}"

    def save(
        self, force_insert=False, force_update=False, using=None, update_fields=None
    ):
        if self.code and len(self.code) < 2:
            self.code = f"0{self.code}"
        super().save(force_insert, force_update, using, update_fields)


class Tender(models.Model):
    name = models.CharField(max_length=255, null=False, blank=False, verbose_name="Название")
    item = models.CharField(max_length=255, null=False, blank=False, verbose_name="Название товара")
    # Customer_inn, Customer_kpp
    contractor = models.ForeignKey(
        "Company",
        on_delete=models.CASCADE,
        related_name="tenders",
        null=False,
        blank=False,
        verbose_name="Заказчик"
    )

    region = models.ForeignKey(
        "Region",
        on_delete=models.CASCADE,
        related_name="tenders",
        null=False,
        blank=False,
        verbose_name="Регион"
    )


class Contract(models.Model):
    STATUS_FINISHED = "finished"
    STATUS_CONCLUDED = "concluded"
    STATUS_DISSOLVED = "dissolved"
    STATUS_REFUSAL_OF_CONCLUSION = "refusal_of_conclusion"

    STATUSES = (
        (STATUS_FINISHED, "Исполнен"),
        (STATUS_CONCLUDED, "Заключен"),
        (STATUS_DISSOLVED, "Расторгнут"),
        (STATUS_REFUSAL_OF_CONCLUSION, "Отказ от заключения"),
    )

    quotation_session = models.ForeignKey(
        "QuotationSession",
        on_delete=models.CASCADE,
        related_name="contracts",
        null=False,
        blank=False,
        verbose_name="Котировочная сессия"
    )

    external_id = models.IntegerField(primary_key=True, unique=True, verbose_name="ID")
    conclusion_datetime = models.DateTimeField(verbose_name="Дата заключения", null=False, blank=False)
    price = models.FloatField(verbose_name="Цена по которой заключен контракт", null=False, blank=False)

    contractor = models.ForeignKey(
        "Company",
        on_delete=models.CASCADE,
        related_name="contracts_as_contractor",
        null=False,
        blank=False,
        verbose_name="Покупатель"
    )
    supplier = models.ForeignKey(
        "Company",
        on_delete=models.CASCADE,
        related_name="contracts_as_supplier",
        null=False,
        blank=False,
        verbose_name="Поставщик"
    )

    violations = models.BooleanField(
        null=False,
        blank=False,
        default=False,
        verbose_name="Наличие нарушений срока подписания контракта"
    )

    status = models.CharField(
        max_length=255,
        choices=STATUSES,
        default=STATUS_CONCLUDED,
        null=False,
        blank=False,
        verbose_name="Статус"
    )


class ContractExecution(models.Model):
    contract = models.ForeignKey(
        "Contract",
        on_delete=models.CASCADE,
        related_name="executions",
        null=False,
        blank=False,
        verbose_name="Контракт"
    )

    external_upd_id = models.IntegerField(null=False, blank=False, verbose_name="ID УПД")
    scheduled_delivery_date = models.DateTimeField(null=False, blank=False, verbose_name="Регламентная дата поставки")
    actual_delivery_date = models.DateTimeField(null=False, blank=False, verbose_name="Фактическая дата поставки")

    delivery_date_delta = models.DurationField(null=False, blank=False, verbose_name="Разница в датах поставки")

    contractor = models.ForeignKey(
        "Company",
        on_delete=models.CASCADE,
        related_name="contract_executions_as_contractor",
        null=False,
        blank=False,
        verbose_name="Покупатель"
    )
    supplier = models.ForeignKey(
        "Company",
        on_delete=models.CASCADE,
        related_name="contract_executions_as_supplier",
        null=False,
        blank=False,
        verbose_name="Поставщик"
    )

    def save(
        self, force_insert=False, force_update=False, using=None, update_fields=None
    ):
        self.delivery_date_delta = self.scheduled_delivery_date - self.actual_delivery_date
        super().save(force_insert, force_update, using, update_fields)

