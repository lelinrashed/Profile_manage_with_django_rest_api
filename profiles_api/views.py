from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from profiles_api.serializers import HelloSerializer, UserProfileSerializer, ProfileFeedItemSerializer
from profiles_api.models import UserProfile, ProfileFeedItem
from profiles_api.permissions import UpdateOwnProfile
from rest_framework.authentication import TokenAuthentication
from rest_framework import filters
from rest_framework.authtoken.serializers import AuthTokenSerializer
from rest_framework.authtoken.views import ObtainAuthToken

# Create your views here.

class HelloApiView(APIView):
    """ Test api view """

    serializer_class = HelloSerializer

    def get(self, request, format=None):
        """ Return a list of APIView features """

        an_apiview = [
            'Uses HTTP methods as function(get, post, patch, put, delete)',
            'It is similar to a traditional Django view',
            'Gives you the most control over your logic',
            'Is mapped mannualy to URLs'
        ]

        return Response({'message': 'Hello', 'an_apiview': an_apiview})



    def post(self, request):
        """ Create a hello message with our name. """

        serializer = HelloSerializer(data=request.data)

        if serializer.is_valid():
            name = serializer.data.get('name')
            message = 'Hello {0}'.format(name)
            return Response({'message': message})

        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    def put(self, request, pk=None):
        """ Handle updating object """

        return Response({'method': 'put'})


    def patch(self, request, pk=None):
        """ Patch request, only update fields provided in the request. """

        return Response({'method': 'patch'})


    def delete(self, request, pk=None):
        """ Delete an objects """

        return Response({'method': 'delete'})



class HelloViewSet(viewsets.ViewSet):
    """ Test API Viewset """

    serializer_class = HelloSerializer

    def list(self, request):
        """ Return a hello message """

        a_viewset = [
            'Uses actions (list, create, retrive, update, partial_update)',
            'Automtically maps to URLs using Routers',
            'Provides more functionality with less code'
        ]

        return Response({'messaeg': 'hello', 'a_viewset': a_viewset})


    def create(self, request):
        """ Create a new hello message """

        serializer = HelloSerializer(data=request.data)

        if serializer.is_valid():
            name = serializer.data.get('name')
            message = 'hello {0}'.format('name')
            return Response({'message': message})
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    def retrieve(self, request, pk=None):
        """ Handle getting and object by it Id """

        return Response({'http_method':'GET'})

    def update(self, request, pk=None):
        """ Handle updating object """

        return Response({'http_method': 'PUT'})

    def patch(self, request, pk=None):
        """ Handle updating part of a an object """

        return Response({'http_method': 'PATCH'})

    def delete(self, request, pk=None):
        """ Destroy an object """

        return Response({'http_method':'DELETE'})



class UserProfileViewSet(viewsets.ModelViewSet):
    """ Handle creating, creating and updating viewset. """

    serializer_class = UserProfileSerializer
    queryset = UserProfile.objects.all()
    authentication_classes = (TokenAuthentication,)
    permission_classes = (UpdateOwnProfile,)
    filter_backends = (filters.SearchFilter,)

    search_fields = ('name', 'email',)



class LoginViewSet(viewsets.ViewSet):
    """ Check email and password and return authtoken. """

    serializer_class = AuthTokenSerializer

    def create(self, request):
        """ Use the ObtainAuthToken APIView and create a token. """

        return ObtainAuthToken().post(request)



class UserProfileFeedViewSet(viewsets.ModelViewSet):
    """ Handles creating, reading, and Updating profiles feed item. """

    authentication_classes = (TokenAuthentication,)
    serializer_class = ProfileFeedItemSerializer
    queryset = ProfileFeedItem.objects.all()


    def perform_create(self, serializer):
        """ Set the user profile to the logged in user. """

        serializer.save(user_profile=self.request.user)

