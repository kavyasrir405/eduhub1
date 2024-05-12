from django.contrib import admin
from .models import CustomUser,Course,CartItem,Payment,Question,Feedback

admin.site.register(CustomUser)
admin.site.register(Course)
admin.site.register(CartItem)
admin.site.register(Payment)
admin.site.register(Question)
admin.site.register(Feedback)




# Register your models here.
