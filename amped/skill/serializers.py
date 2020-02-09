from rest_framework.serializers import ModelSerializer, Serializer
from skill.models import Skill


class RecursiveField(Serializer):
    def to_representation(self, value):
        serializer = self.parent.parent.__class__(value, context=self.context)
        return serializer.data


class SkillSerializer(ModelSerializer):
    sub_skills = RecursiveField(many=True)

    class Meta:
        model = Skill
        fields = ('id', 'name', 'description', 'sub_skills')
