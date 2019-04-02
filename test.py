from breakdown.models import User
from breakdown.serializers import UserSerializer
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from students_breakdown.settings import configure

configure()

user = User(username='qwe')
user.save()

user = User(username='asd')
user.save()


serializer = UserSerializer(user)
print(serializer.data)
