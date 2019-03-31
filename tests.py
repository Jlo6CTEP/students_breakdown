from students_breakdown.urls import router, urlpatterns
from django.urls import include, path
from

def test_adding_routers():
    print(urlpatterns)
    settings.configure()
    return path('', include(router.urls)) in urlpatterns

print(test_adding_routers())