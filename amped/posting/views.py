from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from posting.models import Posting
from posting.pagination import Pagination
from posting.serializers import PostingSerializer


class PostingViewSet(viewsets.ModelViewSet):
    pagination_class = Pagination
    serializer_class = PostingSerializer
    permission_classes = (IsAuthenticated, )

    def get_queryset(self):
        request = self.request
        queryset = Posting.objects.all()

        if self.action in ['update', 'partial_update', 'delete']:
            queryset = queryset.filter(author_id=request.user)

        skill_id = request.query_params.get('skillId', None)
        if skill_id:
            queryset = queryset.filter(required_skills__id=skill_id)
        return queryset.distinct()

