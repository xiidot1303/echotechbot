from django.db import models
import secrets
import string

class PromoCode(models.Model):
    code = models.CharField(max_length=10, unique=True, verbose_name="Kod")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Sana")
    used = models.BooleanField(default=False, verbose_name="Foydalanilgan?")

    def __str__(self):
        return self.code

    @staticmethod
    def generate_code(length=10):
        characters = string.ascii_uppercase + string.digits
        return ''.join(secrets.choice(characters) for _ in range(length))
    
    class Meta:
        verbose_name = "Promokod"
        verbose_name_plural = "Promokodlar"

class UserPromoCode(models.Model):
    user = models.ForeignKey('bot.Bot_user', on_delete=models.CASCADE)
    promo_code = models.ForeignKey(PromoCode, on_delete=models.CASCADE)
    entered_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'promo_code')
    
    def __str__(self):
        return f'{self.user.name} - {self.promo_code.code}'
    
    class Meta:
        verbose_name = "Promokod"
        verbose_name_plural = "Foydalanilgan promokodlar"

