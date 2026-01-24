
from django.dispatch import receiver

from products.models import VariationAttributeValue
from django.db.models.signals import post_save, post_delete

def regenerate_variation_name(variation):
    attrs = variation.attribute_values.select_related("attribute") \
        .order_by("attribute__order")

    name = " / ".join([a.value for a in attrs]) if attrs.exists() else ""

    if variation.name != name:
        variation.name = name
        variation.save(update_fields=["name"])


@receiver(post_save, sender=VariationAttributeValue)
def update_name_on_save(sender, instance, **kwargs):
    regenerate_variation_name(instance.variation_ref)


@receiver(post_delete, sender=VariationAttributeValue)
def update_name_on_delete(sender, instance, **kwargs):
    regenerate_variation_name(instance.variation_ref)



def regenerate_variation_name(variation):
    attrs = variation.attribute_values.select_related("attribute") \
        .order_by("attribute__order")

    name = " / ".join([a.value for a in attrs]) if attrs.exists() else ""

    if variation.name != name:
        variation.name = name
        variation.save(update_fields=["name"])


@receiver(post_save, sender=VariationAttributeValue)
def update_name_on_save(sender, instance, **kwargs):
    regenerate_variation_name(instance.variation)


@receiver(post_delete, sender=VariationAttributeValue)
def update_name_on_delete(sender, instance, **kwargs):
    regenerate_variation_name(instance.variation)