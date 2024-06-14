from rest_framework.generics import CreateAPIView, RetrieveUpdateAPIView
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.settings import api_settings
from users.serializers import UserSerializer, AuthTokenSerializer

class CreateUserView(CreateAPIView):
    serializer_class = UserSerializer
    

class CreateTokenView(ObtainAuthToken):
    serializer_class = AuthTokenSerializer
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES

class ManageUserView(RetrieveUpdateAPIView):
    serializer_class = UserSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    http_method_names = ('get', 'head', 'options', 'patch')

    def get_object(self):
        return self.request.user
    