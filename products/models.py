from django.db import models
from users.models import Consumer, Farmer
# Create your models here.


class Product(models.Model):
    title = models.CharField(max_length=100)
    sub_title = models.CharField(max_length=200)
    main_image = models.ImageField(upload_to="product_main_image/%Y/%m/%d/")
    open = models.BooleanField()

    price = models.IntegerField()
    weight = models.FloatField()
    stock = models.IntegerField()
    instruction = models.TextField(blank=True)

    desc = models.TextField()
    create_at = models.DateTimeField(auto_now_add=True)

    farmer = models.ForeignKey(Farmer, related_name="products", on_delete=models.CASCADE, null=True)
    category = models.ForeignKey(
        'Category', related_name='products', on_delete=models.CASCADE)
    #editor_review = models.ForeignKey(editor_review)

    def __str__(self):
        return self.title


class Product_Image(models.Model):
    product = models.ForeignKey(
        Product, related_name='product_images', on_delete=models.CASCADE)

    image = models.ImageField(
        upload_to="product_images/%Y/%m/%d/", null=True, blank=True)

    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)


class Category(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField()
    parent = models.ForeignKey(
        'self', blank=True, null=True, related_name="children", on_delete=models.CASCADE)

    def __str__(self):
        full_path = [self.name]
        k = self.parent
        while k is not None:
            full_path.append(k.name)
            k = k.parent
        return '->'.join(full_path[::-1])

# class Category(models.Model):
#     KIND_BIG = (
#         ('vege', '채소'),
#         ('fruit', '과일'),
#         ('else', '기타'),
#     )
#     KIND_SMALL_VEGE = (
#         ('potato', '감자'),
#         ('union', '양파'),
#         ('carrot', '당근'),
#         ('sweetp', '고구마'),
#     )
#     KIND_SMALL_FRUIT = (
#         ('apple', '사과'),
#         ('tomato', '토마토'),
#         ('banana', '바나나'),
#         ('pear', '배'),
#     )
#     KIND_SMALL_ELSE = (
#         ('amu', '아무'),
#         ('nothing', '무엇'),
#     )
#     kind_big = models.CharField(max_length=10, choices=KIND_BIG)
#     kind_small_vege = models.CharField(
#         max_length=10, blank=True, choices=KIND_SMALL_VEGE)
#     kind_small_fruit = models.CharField(
#         max_length=10, blank=True, choices=KIND_SMALL_FRUIT)
#     kind_small_else = models.CharField(
#         max_length=10, blank=True, choices=KIND_SMALL_ELSE)


class QnA(models.Model):
    question = models.TextField()
    answer = models.TextField()

    update_at = models.DateTimeField(auto_now=True)
    create_at = models.DateTimeField(auto_now_add=True)

    consumer = models.ForeignKey(
        Consumer, related_name='QnAs', on_delete=models.CASCADE)
    product = models.ForeignKey(
        Product, related_name='QnAs', on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.product.title} - {self.pk}'


def get_delete_product():
    return Product.objects.get_or_create(title="삭제된 상품")[0]