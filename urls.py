from django.conf.urls import url, include
from rest_framework.routers import DefaultRouter
from . import views


router = DefaultRouter()
router.register(r'student', views.StudentViewSet)
router.register(r'lab', views.LabViewSet)
router.register(r'labscheam', views.LabsScheamViewSet)
# router.register(r'labdesk', views.LabDeskViewSet)
router.register(r'timeslot', views.TimeSlotViewSet)
router.register(r'orderrecords', views.OrderRecordsViewSet)
# router.register(r'ationrecords', views.ActionRecordsViewSet)
urlpatterns = [
    url(r'^', include(router.urls)),
    url(r'^labinfos/$', views.labinfos, name='labinfos'),
    url(r'^timeselect/$', views.timeSelect, name='timeselect'),
]
urlpatterns += [url(r'^labdesk/$',
                    views.LabDeskList.as_view(), name='labdesk-list'),
                url(r'^labdesk/(?P<pk>[0-9]+)/$',
                    views.LabDeskDetail.as_view(), name='labdesk-detail'),
                url(r'^queryorderablelabList/(?P<studentID>.+)/$',
                    views.queryOrderableLabList.as_view(),
                    name='studentunorderlab-list'),
                url(r'^hasorderlab/(?P<studentID>.+)/(?P<labID>[0-9]+)/$',
                    views.hasOrderLab.as_view(), name='hasorderlab-list'),
                url(r'^labresourcelist/(?P<labID>[0-9]+)/$',
                    views.labResourceList,
                    name='labresources-list'),
                url(r'^ationrecords/(?P<OrderRecordID__pk>[0-9]+)/$',
                    views.ActionRecordsViewSet.as_view(),
                    name='ationrecords'), ]
