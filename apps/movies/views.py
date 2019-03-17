from rest_framework.viewsets import (ModelViewSet, ReadOnlyModelViewSet)
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAdminUser
from django.db.models import Q
from .models import Movies, Genre
from .serializers import MoviesSerializer, GenreSerializer, MoviesCreateSerializer


class AdminMoviesViewset(ModelViewSet):
    permission_classes = (IsAuthenticated, IsAdminUser)
    queryset = Movies.objects.all()
    serializer_class = MoviesSerializer

    def get_queryset(self):
        q = self.queryset
        # logic for search movies by Name only for admin user
        if 'search' in self.request.query_params:
            search = self.request.query_params['search']
            if search:
                if ' ' not in search:
                    qs = q.filter(name__icontains=search)
                    return qs
        # Return all movies only for admin user
        return q.all()

    # admin can create and update movie
    def create(self, request, *args, **kwargs):
        # logic for update
        if 'id' in request.data:
            movie = self.queryset.filter(id=request.data['id']).first()
            serializer = self.get_serializer(instance=movie, data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response({'result':'success'})

        # create new movie
        serializer = MoviesCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        data = serializer.data
        data['result'] = 'success'
        return Response(data)


class UserMoviesViewset(ReadOnlyModelViewSet):
    permission_classes = (IsAuthenticated,)
    queryset = Movies.objects.all()
    serializer_class = MoviesSerializer

    # this is for normal users
    def get_queryset(self):
        q = self.queryset
        # logic for search movies by Name, any loged in user can use it
        if 'search' in self.request.query_params:
            search = self.request.query_params['search']
            if search:
                if ' ' not in search:
                    qs = q.filter(name__icontains=search)
                    return qs
        # Return all movies, any loged in user can use it
        return q.all()
