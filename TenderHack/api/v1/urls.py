from django.urls import path
from rest_framework import routers

from TenderHack.api.v1 import views

router = routers.SimpleRouter()

router.register(r'regions', views.RegionViewSet)
router.register(r'cpgs', views.CPGSViewSet)
router.register(r'suppliers', views.SubdivisionViewSet)

urlpatterns = router.urls + [
    # path(r'registration/', views.RegistrationApiView.as_view()),
    # path(r'add-view/', views.AddViewApiView.as_view()),
    # path(r'add-company/', views.AddCompanyView.as_view()),
    # path(r'add-feedback/', views.AddFeedbackView.as_view()),
    # path(r'add-support-request/', views.AddSupportView.as_view()),
    # path(r'update-user-profile/', views.UpdateUserProfileView.as_view()),
    # path(r'update-company-profile/', views.UpdateCompanyProfileView.as_view()),
    path(r'inn/', views.INNListApiView.as_view()),
    path(r'kpp/', views.KPPListApiView.as_view()),
]