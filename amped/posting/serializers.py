from rest_framework import serializers
from rest_framework.serializers import ModelSerializer, Serializer
from posting.models import Posting
from skill.models import Skill
from skill.serializers import SkillSerializer
from user.serializers import UserSerializer


class CurrentUserIdDefault(object):
    def set_context(self, serializer_field):
        user = serializer_field.context['request'].user
        self.user_id = user.id
        # self.author = User.objects.get(id=self.userid)

    def __call__(self):
        return self.user_id


class PostingSerializer(ModelSerializer):
    author = UserSerializer(read_only=True)
    author_id = serializers.IntegerField(default=CurrentUserIdDefault(), write_only=True)
    required_skills = SkillSerializer(many=True, read_only=True)
    required_skill_ids = serializers.CharField(write_only=True)

    class Meta:
        model = Posting
        fields = '__all__'

    def create(self, validated_data):
        required_skill_ids = validated_data.pop('required_skill_ids', None)

        instance = super(PostingSerializer, self).create(validated_data)

        if required_skill_ids:
            required_skill_ids = required_skill_ids.split(',')
            if required_skill_ids:
                for sid in required_skill_ids:
                    try:
                        instance.required_skills.add(Skill.objects.get(id=sid))
                    except:
                        pass

        return instance

    def update(self, instance, validated_data):
        required_skill_ids = validated_data.pop('required_skill_ids', None)

        super(PostingSerializer, self).update(instance, validated_data)

        if required_skill_ids:
            required_skill_ids = required_skill_ids.split(',')
            if required_skill_ids:
                instance.required_skills.clear()
                for sid in required_skill_ids:
                    try:
                        instance.required_skills.add(Skill.objects.get(id=sid))
                    except:
                        pass

        return instance
