# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

from rest_framework.generics import (
    get_object_or_404,
    RetrieveUpdateDestroyAPIView,
    RetrieveAPIView)
from rest_framework.permissions import IsAuthenticated, IsAdminUser

from libs.views import ListCreateAPIView
from clusters.models import Cluster, ClusterNode, NodeGPU
from clusters.serializers import (
    ClusterSerializer,
    ClusterNodeSerializer,
    ClusterNodeDetailSerializer,
    GPUSerializer)


class ClusterDetailView(RetrieveAPIView):
    queryset = Cluster.objects.all()
    serializer_class = ClusterSerializer
    permission_classes = (IsAuthenticated, IsAdminUser)

    def get_object(self):
        return Cluster.load()


class ClusterNodeListView(ListCreateAPIView):
    queryset = ClusterNode.objects.all()
    serializer_class = ClusterNodeSerializer
    permission_classes = (IsAuthenticated, IsAdminUser)

    def perform_create(self, serializer):
        serializer.save(cluster=Cluster.load())


class ClusterNodeDetailView(RetrieveUpdateDestroyAPIView):
    queryset = ClusterNode.objects.all()
    serializer_class = ClusterNodeDetailSerializer
    permission_classes = (IsAuthenticated, IsAdminUser)
    lookup_field = 'sequence'


class ClusterNodeGPUViewMixin(object):
    def get_cluster_node(self):
        sequence = self.kwargs['sequence']
        return get_object_or_404(ClusterNode, sequence=sequence)

    def filter_queryset(self, queryset):
        return queryset.filter(cluster_node=self.get_cluster_node())


class ClusterNodeGPUListView(ListCreateAPIView, ClusterNodeGPUViewMixin):
    queryset = NodeGPU.objects.all()
    serializer_class = GPUSerializer
    permission_classes = (IsAuthenticated, IsAdminUser)

    def perform_create(self, serializer):
        serializer.save(cluster_node=self.get_cluster_node())


class ClusterNodeGPUDetailView(RetrieveUpdateDestroyAPIView, ClusterNodeGPUViewMixin):
    queryset = NodeGPU.objects.all()
    serializer_class = GPUSerializer
    permission_classes = (IsAuthenticated, IsAdminUser)
    lookup_field = 'index'
