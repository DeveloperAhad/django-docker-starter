from rest_framework.viewsets import ModelViewSet, ViewSet
from rest_framework.response import Response
from rest_framework import status


class InitialModelViewSet(ModelViewSet):
    def list(self, request):
        return Response(status=status.HTTP_400_BAD_REQUEST)

    def create(self, request):
        return Response(status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk=None):
        return Response(status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk=None):
        return Response(status=status.HTTP_400_BAD_REQUEST)

    def partial_update(self, request, pk=None):
        return Response(status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None):
        return Response(status=status.HTTP_400_BAD_REQUEST)


class InitialViewSet(ViewSet):
    def list(self, request):
        return Response(status=status.HTTP_400_BAD_REQUEST)

    def create(self, request):
        return Response(status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk=None):
        return Response(status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk=None):
        return Response(status=status.HTTP_400_BAD_REQUEST)

    def partial_update(self, request, pk=None):
        return Response(status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None):
        return Response(status=status.HTTP_400_BAD_REQUEST)