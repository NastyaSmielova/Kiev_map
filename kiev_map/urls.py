from django.conf.urls import url
from django.contrib import admin
from . import views
from django.conf.urls import (
handler400, handler403, handler404, handler500
)

app_name = 'kiev_map'
handler404 = 'kiev_map.views.custom_404'
handler500 = 'kiev_map.views.custom_500'


urlpatterns = [
    url(r'^admin/',admin.site.urls),
    url(r'^mainPage/',views.main_page, name='main_page'),
    url(r'^district/(?P<pk_district>\d+)$', views.district_id, name='district_id'),
    url(r'^districts/$', views.districts, name='districts'),
    url(r'^street/(?P<pk_street>\d+)$', views.street_id, name='street_id'),
    url(r'^streets/$', views.streets, name='streets'),
    url(r'^streets_by_district/(?P<pk_district>\d+)$', views.streets_by_district, name='streets_by_district'),
    url(r'^quiz/$', views.quiz, name='quiz'),

]