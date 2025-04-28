from django.shortcuts import render

# Create your views here.
# views.py
from rest_framework import viewsets
from .models import Review
from .serializers import ReviewSerializer
from rest_framework.response import Response
from rest_framework.decorators import action

# ViewSet لعرض وتعديل وحذف التقييمات
class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all()  # استرجاع جميع التقييمات
    serializer_class = ReviewSerializer  # استخدم الـ Serializer الذي سننشئه

    # دالة لحذف التقييم عبر API
    @action(detail=True, methods=['delete'])
    def delete_review(self, request, pk=None):
        review = self.get_object()
        review.delete()
        return Response({'message': 'Review deleted successfully'}, status=204)

    # دالة لتعديل التقييم عبر API
    @action(detail=True, methods=['put'])
    def update_review(self, request, pk=None):
        review = self.get_object()
        serializer = self.get_serializer(review, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=200)
        return Response(serializer.errors, status=400)
