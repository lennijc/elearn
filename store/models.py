from django.db import models
from django.contrib.auth import get_user_model
# Create your models here.

User=get_user_model()

class comment(models.Model):
    body = models.TextField()
    course = models.ForeignKey("courses",on_delete=models.SET_NULL,null=True,blank=True)
    article = models.ForeignKey("article",on_delete=models.SET_NULL,null=True,blank=True)
    creator = models.ForeignKey(User,on_delete=models.SET_NULL,null=True)
    createdAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now=True)
    answer=models.IntegerField()
    isAnswer=models.BooleanField()
    SCORE_CHOICES=[
        ("1","one"),
        ("2","two"),
        ("3","three"),
        ("4","four"),
        ("5","five"),
    ]
    score=models.CharField(max_length=1,choices=SCORE_CHOICES)
    def __str__(self) -> str:
        return str(self.creator)


class article(models.Model):
    title=models.CharField(max_length=255)
    description=models.TextField()
    body=models.CharField(max_length=255)
    cover=models.ImageField(null=True,blank=True)
    href=models.CharField(max_length=255,unique=True)
    category=models.ForeignKey("categories",on_delete=models.PROTECT)
    creator=models.ForeignKey(User,on_delete=models.SET_NULL,null=True)
    createdAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now=True)
    publish=models.BooleanField()
    def __str__(self) -> str:
        return self.title
    
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
    href=models.CharField(max_length=255,unique=True)
    categoryID=models.ForeignKey(categories,on_delete=models.PROTECT,related_name="subMenu")
    creator=models.ForeignKey(User,on_delete=models.PROTECT,null=True,blank=True)
    createdAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now=True)
    student = models.ManyToManyField(User,through="courseUser",through_fields=('course','user'),related_name="student_user")
    isComplete=models.BooleanField()
    price=models.PositiveIntegerField(default=0)
    def __str__(self):
        return self.href

class courseUser(models.Model):
    course = models.ForeignKey(courses,on_delete=models.CASCADE)
    user= models.ForeignKey(User,on_delete=models.PROTECT)
    createdAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now=True)
    def __str__(self) -> str:
        return str(self.course)
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['course', 'user'], name='cannot_register_twice'),
        ]

class session(models.Model):
    title=models.CharField(max_length=255)
    course=models.ForeignKey(courses,on_delete=models.CASCADE)
    createdAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now=True)
    time=models.DurationField(help_text="total duration of a vidoe clip")
    free = models.BooleanField()
    def __str__(self):
        return self.title
    
class notification(models.Model):
    msg = models.TextField()
    admin=models.ForeignKey(User,on_delete=models.SET_NULL,null=True)
    createdAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now=True)
    see=models.BooleanField(default=False)
    def __str__(self):
        return self.msg

class menus(models.Model):
    title = models.CharField(max_length=255)
    href = models.CharField(max_length=255)
    createdAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.title
    
class contact(models.Model):
    name=models.CharField(max_length=255)
    email= models.EmailField()
    phone=models.CharField(max_length=11,null=True)
    body=models.TextField()        
    createdAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now=True)
    answer=models.BooleanField(default=False)
    def __str__(self):
        return self.name

class orderModel(models.Model):
    course=models.ForeignKey(courses,on_delete=models.PROTECT)
    user=models.ForeignKey(User,on_delete=models.SET_NULL,null=True)
    createdAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now=True)
    price=models.PositiveIntegerField(default=0)
    def __str__(self):
        return  f"{self.course}"
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['course', 'user'], name='already ordered and registered in this course'),
        ]
    

    
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
    




    
