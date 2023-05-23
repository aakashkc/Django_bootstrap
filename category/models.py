from django.db import models
from django.urls import reverse

# Create your models here.

# Create your models here.

class Category(models.Model):
    category_name=models.CharField(max_length=50, unique=True)
    slug=models.SlugField(max_length=100, unique=True)
    description=models.TextField(max_length=255, blank=True)
    cat_image=models.ImageField(upload_to='static/images/category', blank=True)

    #to change the Category into categories in admin pannel
    class Meta:
        verbose_name='category'
        verbose_name_plural='categories'

        # verbose A human-readable name for the field.
        #  If the verbose name isn’t given,
        #  Django will automatically create it using the field’s attribute name,
        #  converting underscores to spaces.

    def get_url(self):

        return reverse('product_by_category', args=[self.slug])







    #string representation of model
    def __str__(self):
        return self.category_name