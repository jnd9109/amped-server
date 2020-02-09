from rest_framework.serializers import ModelSerializer, Serializer
from skill.models import Skill


class SubCategorySerializer(ModelSerializer):
    class Meta:
        model = Skill
        fields = ('id', 'name', 'description')


class SkillSerializer(ModelSerializer):
    sub_skills = SubCategorySerializer(many=True)

    class Meta:
        model = Skill
        fields = ('id', 'name', 'description', 'sub_skills')
