from django.db import models
import secrets
import string
from asgiref.sync import sync_to_async

class PromoCode(models.Model):
    code = models.CharField(max_length=10, unique=True, verbose_name="Kod")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Sana")
    used = models.BooleanField(default=False, verbose_name="Foydalanilgan?")

    def __str__(self):
        return self.code

    async def set_as_used(self):
        self.used = True
        await self.asave()

    @staticmethod
    def generate_code(length=10):
        characters = string.ascii_uppercase + string.digits
        return ''.join(secrets.choice(characters) for _ in range(length))
    
    class Meta:
        verbose_name = "Promokod"
        verbose_name_plural = "Promokodlar"

class UserPromoCode(models.Model):
    user = models.ForeignKey('bot.Bot_user', on_delete=models.CASCADE)
    promo_code = models.ForeignKey(PromoCode, on_delete=models.CASCADE, verbose_name='Promokod')
    entered_at = models.DateTimeField(auto_now_add=True, verbose_name='Foydalanilgan sana')

    class Meta:
        unique_together = ('user', 'promo_code')
    
    def __str__(self):
        return f'{self.user.name} - {self.promo_code.code}'
    
    class Meta:
        verbose_name = "Promokod"
        verbose_name_plural = "Foydalanilgan promokodlar"


class Statement(models.Model):
    bot_user = models.ForeignKey('bot.Bot_user', on_delete=models.CASCADE, verbose_name='Foydalanuvchi')
    promocode = models.OneToOneField(PromoCode, on_delete=models.CASCADE, verbose_name='Promokod')
    photo = models.FileField(upload_to='statements/', verbose_name='Rasm', null=True)
    confirmed = models.BooleanField(default=False, verbose_name='Tasdiqlandi?')
    datetime = models.DateTimeField(auto_now_add=True, verbose_name='Sana')

    @property
    @sync_to_async
    def get_promocode(self) -> PromoCode:
        return self.promocode
    
    @property
    @sync_to_async
    def get_bot_user(self):
        return self.bot_user

    class Meta:
        verbose_name = "Ariza"
        verbose_name_plural = "Arizalar"