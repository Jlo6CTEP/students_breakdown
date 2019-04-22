from breakdown.models import User
from breakdown.serializers import UserSerializer
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser


user = User.objects.create_user('myusername', 'myemail@crazymail.com', 'mypassword')
user.save()
serializer = UserSerializer(user)
print(serializer.data)
