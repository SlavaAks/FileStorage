from file.views import FileViewset
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'upload', FileViewset, basename='file')
urlpatterns = router.urls