from django.conf.urls import url, include
from rest_framework.routers import DefaultRouter
from . import views


router = DefaultRouter()
router.register(r'student', views.StudentViewSet)
router.register(r'lab', views.LabViewSet)
router.register(r'labscheam', views.LabsScheamViewSet)
# router.register(r'labdesk', views.LabDeskViewSet)
router.register(r'timeslot', views.TimeSlotViewSet)
router.register(r'records', views.RecordsViewSet)
urlpatterns = [
    url(r'^', include(router.urls)),
    url(r'^labinfos/$', views.labinfos, name='labinfos'),
    url(r'^timeselect/$', views.timeSelect, name='timeselect'),
]
urlpatterns += [url(r'^labdesk/$',
                    views.LabDeskList.as_view(), name='labdesk-list'),
                url(r'^labdesk/(?P<pk>[0-9]+)/$',
                    views.LabDeskDetail.as_view(), name='labdesk-detail'),
                url(r'^studentunorderlab/(?P<studentID>.+)/$',
                    views.StudentUnorderLabList.as_view(),
                    name='studentunorderlab-list'),
                url(r'^labresources/(?P<studentID>.+)/(?P<labID>[0-9]+)/$',
                    views.LabResourcesList,
                    name='labresources-list'), ]
