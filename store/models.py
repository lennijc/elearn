from django.db import models
from django.contrib.auth import get_user_model
# Create your models here.

User=get_user_model()

class article(models.Model):
    title=models.CharField(max_length=255)
    description=models.TextField()
    body=models.CharField(max_length=255)
    cover=models.ImageField()
    shortName=models.CharField(max_length=255)
    category=models.ForeignKey("categories",on_delete=models.PROTECT)
    creator=models.ForeignKey(User,on_delete=models.SET_NULL,null=True)
    createdAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now=True)
    publish=models.BooleanField()

class categories(models.Model):
    title=models.CharField(max_length=255)
    createdAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now=True)
    name=models.CharField(max_length=255)
    def __str__(self):
        return self.title
class courses(models.Model):
    name=models.CharField(max_length=255)
    description=models.TextField(null=True , blank=True)
    cover = models.ImageField(null=True , blank=True)
    shortName=models.CharField(max_length=255)
    categoryID=models.ForeignKey(categories,on_delete=models.PROTECT)
    creator=models.ForeignKey(User,on_delete=models.PROTECT,null=True,blank=True)
    createdAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now=True)
    isComplete=models.BooleanField()
    def __str__(self):
        return self.shortName
class menus(models.Model):
    title = models.CharField(max_length=255)
    href = models.CharField(max_length=255)
    createdAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.title
        



class promotions(models.Model):
    description = models.CharField(max_length=255)
    discount = models.FloatField()


class product(models.Model):
    title = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    inventory = models.IntegerField()
    price = models.DecimalField(max_digits=6 , decimal_places=2)
    collection = models.ForeignKey('collection' , on_delete=models.PROTECT)
    last_update = models.DateTimeField(auto_now=True)
    promotion = models.ManyToManyField(promotions)


class collection(models.Model):
    title = models.CharField(max_length=255)
    featured_product = models.ForeignKey(product , on_delete=models.SET_NULL ,null = True , related_name='+')

    def __str__(self):
        return self.title
    

class Customer(models.Model):
   first_name = models.CharField(max_length=255)
   last_name = models.CharField(max_length=255)
   email = models.CharField(unique=True , max_length=255 )
   phone = models.CharField(max_length=255)
   birth_date = models.DateField(null=True)


class Order(models.Model):
    placed_at = models.DateTimeField(auto_now_add=True)
    PAYMENT_STAUS_PENDING = "P"
    PAYMENT_STAUS_Complete = "C"
    PAYMENT_STAUS_Failed= "F"
    PAYMENT_STATUS_CHOICES = [
        (PAYMENT_STAUS_PENDING,"Pending"),
        (PAYMENT_STAUS_Complete,"Complete"),
        (PAYMENT_STAUS_Failed,"Failed"),
    ]
    payment_status = models.CharField(max_length= 1 , choices=PAYMENT_STATUS_CHOICES , default = PAYMENT_STAUS_PENDING )
    item = models.ForeignKey(product , on_delete= models.PROTECT)
    customer= models.ForeignKey(Customer , on_delete= models.PROTECT)
    
class OrderItem(models.Model):
    Order = models.ForeignKey(Order,on_delete=models.PROTECT)
    product = models.ForeignKey(product , on_delete=models.PROTECT)
    quantity = models.PositiveSmallIntegerField()
    unit_price = models.DecimalField(max_digits=6 , decimal_places=2)

class Address(models.Model):
    street=models.CharField(max_length=255)
    city=models.CharField(max_length=255)
    customer=models.OneToOneField(Customer, on_delete=models.CASCADE)
    zip = models.CharField(max_length=10 , null=True)
    


class cart(models.Model):
    created_at = models.DateTimeField(auto_now_add = True)

class cartItem(models.Model):
    cart =  models.ForeignKey(cart , on_delete = models.CASCADE)
    product = models.ForeignKey(product , on_delete = models.CASCADE)
    quantity = models.PositiveSmallIntegerField()






    
