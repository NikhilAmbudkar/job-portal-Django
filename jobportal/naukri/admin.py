from django.contrib import admin
from . models import DetailJob,DetailData,Profile
# Register your models here.


class DetailJobAdmin(admin.ModelAdmin):
    list_display=['jname','jdesc','company','location','salary','experience','skills']


class DetailDataAdmin(admin.ModelAdmin):
    list_display=['fname','lname','contact','email','edu','file','address']

class ProfileAdmin(admin.ModelAdmin):
    list_display=['user','bio','profile_picture','birthdate','mobile_number']


admin.site.register(DetailJob,DetailJobAdmin)
admin.site.register(DetailData,DetailDataAdmin)
admin.site.register(Profile,ProfileAdmin)