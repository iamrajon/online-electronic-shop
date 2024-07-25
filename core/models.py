from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator


# model for Customer 
STATE_CHOICES = (
    ('s1 Purwanchal pradesh', 'Purwanchal Pradesh'),
    ('s2 Madhesh pradesh', 'Madhesh Pradesh'),
    ('s3 Bagmati pradesh', 'Bagmati Pradesh'),
    ('s4 Gandaki  pradesh', 'Gandaki Pradesh'),
    ('s5 Lumbini pradesh', 'Lumbini Pradesh'),
    ('s6 Karnali pradesh', 'Karnali Pradesh'),
    ('s7 Sudur Pashchim pradesh', 'Sudur Paschim Pradesh'),
)

class Customer(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length = 100)
    phone = models.CharField(max_length = 15)
    city = models.CharField(max_length = 100)
    locality = models.CharField(max_length = 150)
    zipcode = models.IntegerField(blank=True)
    state = models.CharField(choices=STATE_CHOICES, max_length=100)

    def __str__(self):
        return str(self.id)
    

# model for Product
CATEGORY_CHOICES = (
    ('M', 'Mobile'),
    ('L', 'Laptop'),
    ('H', 'HeadPhone'),
    ('W', 'Watch'),
    ('E', 'Electronic'),
    ('T', 'Trending'),
    ('O', 'Other'),
)

class Product(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    brand = models.CharField(max_length=100)
    selling_price = models.FloatField()
    discounted_price = models.FloatField()
    category = models.CharField( choices=CATEGORY_CHOICES, max_length=2)
    product_image = models.ImageField(upload_to="productimg")

    def __str__(self):
        return str(self.id)
    
    
# model for Cart
class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    

    def __str__(self):
        return str(self.id)
    
    @property
    def total_cost(self):
        return self.quantity * self.product.discounted_price
    

    

# model for OrderPlaced
STATUS_CHOICES = (
    ('Accepted', 'Accepted'),
    ('Packed', 'Packed'),
    ('On The Way', 'On The Way'),
    ('Delivered', 'Delivered'),
    ('Cancel', 'Cancel'),
)
class OrderPlaced(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    ordered_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='pending')

    def __str__(self):
        return str(self.id)
    
    @property
    def total_cost(self):
        return self.quantity * self.product.discounted_price
    
    

