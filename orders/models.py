from django.db      import models
from django.db.models.deletion import CASCADE
from core.models    import TimeStampModel

# Create your models here.
class Cart(models.Model) :
    user    = models.ForeignKey('users.User', on_delete=CASCADE, related_name='cart_by_user')
    course  = models.ForeignKey('courses.Course', on_delete=CASCADE, related_name='cart_by_course')
    
    class Meta :
        db_table = 'carts'

class Order(TimeStampModel) :
    user    = models.ForeignKey('users.User', on_delete=CASCADE, related_name='order')
    
    class Meta :
        db_table = 'carts'

class OrderItem(TimeStampModel) :
    order   = models.ForeignKey('Order', on_delete=CASCADE , related_name='order_item_by_order')
    course  = models.ForeignKey('courses.Course', on_delete=CASCADE, related_name='order_item_by_course')
    
    class Meta :
        db_table = 'carts'

