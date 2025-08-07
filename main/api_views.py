from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from django.shortcuts import get_object_or_404
from .models import CV
from .serializers import CVSerializer, CVListSerializer


class CVListCreateView(ListCreateAPIView):
    """API view for listing and creating CVs."""
    
    queryset = CV.objects.all().order_by('-created_at')
    serializer_class = CVListSerializer
    
    def get_serializer_class(self):
        """Use different serializers for GET and POST."""
        if self.request.method == 'POST':
            return CVSerializer
        return CVListSerializer


class CVDetailView(RetrieveUpdateDestroyAPIView):
    """API view for retrieving, updating, and deleting a single CV."""
    
    queryset = CV.objects.all()
    serializer_class = CVSerializer
    lookup_field = 'pk'


@api_view(['GET', 'POST'])
def cv_list_api(request):
    """Function-based API view for CV list and creation."""
    if request.method == 'GET':
        cvs = CV.objects.all().order_by('-created_at')
        serializer = CVListSerializer(cvs, many=True)
        return Response(serializer.data)
    
    elif request.method == 'POST':
        serializer = CVSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
def cv_detail_api(request, pk):
    """Function-based API view for CV detail, update, and deletion."""
    cv = get_object_or_404(CV, pk=pk)
    
    if request.method == 'GET':
        serializer = CVSerializer(cv)
        return Response(serializer.data)
    
    elif request.method == 'PUT':
        serializer = CVSerializer(cv, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    elif request.method == 'DELETE':
        cv.delete()
        return Response(status=status.HTTP_204_NO_CONTENT) 