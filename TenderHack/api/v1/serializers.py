import datetime

from rest_framework import serializers

from TenderHack.models import Region, CPGS, Subdivision


class RegionSerializer(serializers.ModelSerializer):
    id = serializers.SerializerMethodField()

    class Meta:
        model = Region
        fields = [
            "id",
            "name",
        ]

    def get_id(self, obj):
        return obj.pk


class CPGSSelectSerializer(serializers.ModelSerializer):
    id = serializers.SerializerMethodField()
    text = serializers.SerializerMethodField()

    class Meta:
        model = CPGS
        fields = [
            "id",
            "text"
        ]

    def get_id(self, obj):
        return obj.id

    def get_text(self, obj):
        return f"{obj.full_path} {obj.name}"


class SubdivisionSerializer(serializers.ModelSerializer):
    # last_tender_participation_metric = serializers.SerializerMethodField()

    class Meta:
        model = Subdivision
        fields = [
            "kpp",
            "is_supplier",
            "is_contractor",
            "creation_datetime",
            "date_delta",
            "company",
            # "last_tender_participation_metric"
        ]

    # def get_last_tender_participation_metric(self, obj):
    #     return obj.last_tender_participation_metric
