from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.core.cache import cache


@receiver(post_save)
def invalidate_cache_on_save(sender, instance, created, **kwargs):
    """Invalidate cache when model is saved"""
    model_name = sender.__name__
    cache.delete_many([f"{model_name}:*"])

    if hasattr(instance, "user_id"):
        cache.delete_many([f"*:{instance.user_id}:*"])


@receiver(post_delete)
def invalidate_cache_on_delete(sender, instance, **kwargs):
    """Invalidate cache when model is deleted"""
    model_name = sender.__name__
    cache.delete_many([f"{model_name}:*"])

    if hasattr(instance, "user_id"):
        cache.delete_many([f"*:{instance.user_id}:*"])
