from django.urls import path
from . import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register("collection", views.CollectionViewSet, basename="collection")
router.register("job_group", views.JobGroupViewSet)
router.register("operation_lib", views.OperationLibViewSet, basename="operation_lib")
router.register("operation_list", views.OperationListViewSet, basename="operation_list")
router.register("element_lib", views.ElementLibViewSet, basename="element_lib")
router.register("element_list", views.ElementListItemViewSet, basename="element_list")
router.register("time_study", views.TimeStudyViewSet)

urlpatterns = router.urls
