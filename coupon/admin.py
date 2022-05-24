from django.contrib import admin
from coupon.models import Coupon, CouponUser

# Register your models here.


admin.site.register(Coupon)
admin.site.register(CouponUser)