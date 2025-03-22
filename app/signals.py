from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from app.models import Statement
from app.services.statement_service import statement_confirm, statement_deleted
from asgiref.sync import async_to_sync



@receiver(post_save, sender=Statement)
def statement_confirmed_handler(sender, instance, **kwargs):
    if instance.confirmed:
        async_to_sync(statement_confirm)(instance)

@receiver(post_delete, sender=Statement)
def statement_deleted_handler(sender, instance, **kwargs):
    async_to_sync(statement_deleted)(instance)
