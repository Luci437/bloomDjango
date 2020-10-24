from django.urls import path, include
from bloomapp import views

urlpatterns = [
    path('', views.login, name='login'),
    path('signup/', views.signup, name='signup'),
    path('signup/checkUsername/', views.checkUsername, name="checkUsername"),
    path('joinGroup/', views.joinGroup, name="joinGroup"),
    path('createGroup/', views.createGroup, name="createGroup"),
    path('<int:group_id>/group/', views.showGroup, name="group"),
    path('showMyGroup/', views.showMyGroups, name="showMyGroup"),
    path('logout/', views.logout, name="logout"),
    path('addReview/', views.addReview, name='addReview'),
    path('showMyReview/', views.showReviews, name='showMyReview'),
    path('<int:review_id>/markAsReview/', views.markAsRead, name="markAsRead"),
    path('<int:group_id>/changeGroupPermission/', views.changeGroupPermission, name="changeGroupPermission")
]