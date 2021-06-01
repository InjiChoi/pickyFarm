from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Product_Comment
from admins.models import FarmerNotification


@receiver(post_save, sender=Product_Comment)
def product_comment_post_save(sender, instance, **kwargs):
    FarmerNotification.objects.create(
        farmer=instance.product.farmer,
        message="상품 " + "'" + instance.product.title + "'" + "의 리뷰가 등록되었습니다.",
        notitype="review_noti",
        obj_pk=instance.pk,
    )
