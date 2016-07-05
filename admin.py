from django.contrib import admin
from .models import TimeSlot, LabDesk, Parameter, LabCategory
from .models import Instrument, Lab, OrderRecords, Student, LabsScheam
from .models import ActionRecords
# Register your models here.


class ParameterAdmin(admin.ModelAdmin):
    list_display = ('preDay', 'mostDay')


class LabDeskAdmin(admin.ModelAdmin):
    list_display = ('pk', 'deskID', 'labCategory')


class LabAdmin(admin.ModelAdmin):
    list_display = ('pk', 'labName', 'labCategory', 'startDate', 'endDate')


class InstrumentAdmin(admin.ModelAdmin):
    list_display = ('ID', 'name', 'Position', 'URL')


class StudentAdmin(admin.ModelAdmin):
    list_display = ('studentID', 'name', 'labscheam')


class OrderRecordsAdmin(admin.ModelAdmin):
    list_display = (
        'deskID', 'date', 'timeSlot', 'student', 'orderTime', 'updateTime', 'lab')


class ActionRecordsAdmin(admin.ModelAdmin):
    list_display = ('OrderRecordID', 'actionTime', 'action')


class LabScheamAdmin(admin.ModelAdmin):
    filter_horizontal = ('labs',)

admin.site.register(TimeSlot)
admin.site.register(Instrument, InstrumentAdmin)
admin.site.register(Lab, LabAdmin)
admin.site.register(LabCategory)
admin.site.register(Parameter, ParameterAdmin)
admin.site.register(LabDesk, LabDeskAdmin)
admin.site.register(OrderRecords, OrderRecordsAdmin)
admin.site.register(Student, StudentAdmin)
admin.site.register(LabsScheam, LabScheamAdmin)
admin.site.register(ActionRecords, ActionRecordsAdmin)
