from django.conf.urls import url
from crawlzero import views
# SET THE NAMESPACE!
app_name = 'crawlzero'
# Be careful setting the name to just /login use userlogin instead!
urlpatterns=[
    url(r'^register/$',views.register,name='register'),
    url(r'^user_login/$',views.user_login,name='user_login'),
    url(r'^upload_file/$',views.upload_file,name='upload_file'),
    
]