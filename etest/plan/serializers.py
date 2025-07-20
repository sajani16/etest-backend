from plan.models import Plan
from rest_framework import serializers

class PlanSerializer(serializers.ModelSerializer):
    class Meta:
        model = Plan
        fields = '__all__'