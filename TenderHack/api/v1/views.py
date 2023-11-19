import json

import django_filters
from django.db.models import Max
from django.http import QueryDict
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import mixins, viewsets, filters
from rest_framework.filters import OrderingFilter
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.response import Response
from rest_framework.views import APIView
import numpy as np


from TenderHack.api.v1.serializers import RegionSerializer, CPGSSelectSerializer, SubdivisionSerializer
from TenderHack.models import Region, CPGS, Subdivision, Company, Tender


class RegionViewSet(mixins.ListModelMixin,
                    viewsets.GenericViewSet):
    serializer_class = RegionSerializer
    queryset = Region.objects.all()
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, OrderingFilter]
    # pagination_class = LimitOffsetPagination
    search_fields = ['name']
    filterset_fields = ["name", "code"]
    ordering_fields = "__all__"
    ordering = ["name"]


class CPGSViewSet(mixins.ListModelMixin,
                  viewsets.GenericViewSet):
    serializer_class = CPGSSelectSerializer
    queryset = CPGS.objects.all()
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, OrderingFilter]
    pagination_class = LimitOffsetPagination
    search_fields = ['full_path', "code", "name"]
    filterset_fields = ["name", "code"]
    ordering_fields = "__all__"
    ordering = ["name"]


class SubdivisionFilter(django_filters.FilterSet):
    queryset = Subdivision.objects.filter(is_supplier=True, participation__isnull=False)

    kpp = django_filters.ModelMultipleChoiceFilter(
        field_name="kpp",
        queryset=queryset,
        lookup_expr="exact",
        conjoined=False,
    )

    company__inn = django_filters.ModelMultipleChoiceFilter(
        field_name="company__inn",
        queryset=Company.objects.all(),
        lookup_expr="exact",
        conjoined=False,
    )

    participation__tender__region__code = django_filters.ModelMultipleChoiceFilter(
        field_name="participation__tender__region__code",
        queryset=Region.objects.all(),
        lookup_expr="exact",
        conjoined=False,
    )
    participation__tender__CPGSs__id = django_filters.ModelMultipleChoiceFilter(
        field_name="participation__tender__CPGSs__id",
        queryset=CPGS.objects.all(),
        lookup_expr="exact",
        conjoined=False,
    )
    participation__tender__date_created__lte = django_filters.ModelMultipleChoiceFilter(
        field_name="participation__tender__date_created__lte",
        queryset=Tender.objects.all(),
        lookup_expr="lte",
        conjoined=False,
    )

    participation__tender__date_created__gte = django_filters.ModelMultipleChoiceFilter(
        field_name="participation__tender__date_created__gte",
        queryset=Tender.objects.all(),
        lookup_expr="gte",
        conjoined=False,
    )

    class Meta:
        model = Subdivision
        fields = [
            "kpp",
            "company__inn",
            "participation__tender__region__code",
            "participation__tender__CPGSs__id",
            "participation__tender__date_created__lte",
            "participation__tender__date_created__gte",
        ]


class SubdivisionViewSet(mixins.ListModelMixin,
                         viewsets.GenericViewSet):

    serializer_class = SubdivisionSerializer
    queryset = Subdivision.objects.filter(is_supplier=True, participation__isnull=False)
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, OrderingFilter]
    pagination_class = LimitOffsetPagination
    search_fields = ["participation__tender__name, participation__tender__items__name"]
    # filterset_class = SubdivisionFilter
    ordering = ["date_delta"]

    def list(self, request, *args, **kwargs):
        print(0)
        queryset = self.filter_queryset(self.get_queryset())
        if request.GET.get("kpp"):
            queryset = queryset.filter(kpp=request.GET.get("kpp"))
        if request.GET.get("inn"):
            queryset = queryset.filter(company__inn=request.GET.get("inn"))
        if request.GET.get("tags"):
            tags = request.GET.getlist("tags")
            for tag in tags:
                queryset = queryset | queryset.filter(participation__tender__items__name__contains=tag)
        queryset = queryset.distinct()

        queryset = queryset.values("pk").annotate(max_per_prod=Max("participation__tender__date_created"))
        queryset = list(queryset.values_list("pk", flat=True))

        queryset = Subdivision.objects.filter(pk__in=queryset).order_by("date_delta")

        points_list = np.linspace(1, 0, len(queryset)).tolist()

        for idx, el in enumerate(points_list):
            queryset[idx].last_tender_participation_metric = el
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class INNListApiView(APIView):
    def get(self, request):
        qs = Company.objects.all().values("id", "inn")
        if request.GET.get("search"):
            qs = qs.filter(inn__contains=request.GET.get("search"))
        data = list(qs.distinct()[:10])
        return Response(data)


class KPPListApiView(APIView):
    def get(self, request):
        qs = Subdivision.objects.all()
        if request.GET.get("search"):
            qs = qs.filter(kpp__contains=request.GET.get("search"))
        data = list(qs.values("id", "kpp").distinct()[:10])
        print(data)
        return Response(data)



