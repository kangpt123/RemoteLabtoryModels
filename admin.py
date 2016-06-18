from django.contrib import admin
from .models import TimeSlot, LabDesk, Parameter, LabCategory
from .models import Instrument, Lab, Records, Student, LabsScheam
# Register your models here.


class ParameterAdmin(admin.ModelAdmin):
    list_display = ('preDay', 'mostDay')


class LabDeskAdmin(admin.ModelAdmin):
    list_display = ('deskID', 'labCategory')


class LabAdmin(admin.ModelAdmin):
    list_display = ('labName', 'labCategory', 'startDate', 'endDate')


class InstrumentAdmin(admin.ModelAdmin):
    list_display = ('ID', 'name', 'Position')


class StudentAdmin(admin.ModelAdmin):
    filter_horizontal = ('finishLabs',)
    list_display = ('studentID', 'name', 'labscheam')


class ResourcesAdmin(admin.ModelAdmin):
    list_display = ('deskID', 'date', 'timeSlot', 'student', 'orderTime')


class LabScheamAdmin(admin.ModelAdmin):
    filter_horizontal = ('labs',)

admin.site.register(TimeSlot)
admin.site.register(Instrument, InstrumentAdmin)
admin.site.register(Lab, LabAdmin)
admin.site.register(LabCategory)
admin.site.register(Parameter, ParameterAdmin)
admin.site.register(LabDesk, LabDeskAdmin)
admin.site.register(Records, ResourcesAdmin)
admin.site.register(Student, StudentAdmin)
admin.site.register(LabsScheam, LabScheamAdmin)
