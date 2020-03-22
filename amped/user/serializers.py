from django.contrib.auth import authenticate, get_user_model
from django.conf import settings
from django.contrib.auth.models import Group
from django.utils.translation import ugettext_lazy as _

from rest_framework import serializers, exceptions, status

from skill.models import Skill
from skill.serializers import SkillSerializer
from user.models import User

UserModel = get_user_model()


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField(required=False, allow_blank=True)
    password = serializers.CharField(style={'input_type': 'password'})

    def authenticate(self, **kwargs):
        return authenticate(self.context['request'], **kwargs)

    def _validate_email(self, email, password):
        user = None

        if email and password:
            user = self.authenticate(email=email, password=password)
        else:
            msg = _('Must include "email" and "password".')
            raise exceptions.ValidationError(msg)

        return user

    def _validate_username(self, username, password):
        user = None

        if username and password:
            user = self.authenticate(username=username, password=password)
        else:
            msg = _('Must include "username" and "password".')
            raise exceptions.ValidationError(msg)

        return user

    def _validate_username_email(self, username, email, password):
        user = None

        if email and password:
            user = self.authenticate(email=email, password=password)
        elif username and password:
            user = self.authenticate(username=username, password=password)
        else:
            msg = _('Must include either "username" or "email" and "password".')
            raise exceptions.ValidationError(msg)

        return user

    def validate(self, attrs):
        username = attrs.get('username')
        email = attrs.get('email')
        password = attrs.get('password')

        user = None

        if 'allauth' in settings.INSTALLED_APPS:
            from allauth.account import app_settings

            # Authentication through email
            if app_settings.AUTHENTICATION_METHOD == app_settings.AuthenticationMethod.EMAIL:
                user = self._validate_email(email, password)

            # Authentication through either username or email
            else:
                user = self._validate_username_email(username, email, password)

        else:
            # Authentication without using allauth
            if email:
                try:
                    username = UserModel.objects.get(email__iexact=email).get_username()
                except UserModel.DoesNotExist:
                    pass

            if username:
                user = self._validate_username_email(username, '', password)

        # Did we get back an active user?
        if user:
            if not user.is_active:
                msg = _('User account is disabled.')
                raise exceptions.ValidationError(msg, code=status.HTTP_401_UNAUTHORIZED)
        else:
            msg = _('Unable to log in with provided credentials.')
            raise exceptions.ValidationError(msg, code=status.HTTP_401_UNAUTHORIZED)

        # If required, is the email verified?
        if 'rest_auth.registration' in settings.INSTALLED_APPS:
            from allauth.account import app_settings
            if app_settings.EMAIL_VERIFICATION == app_settings.EmailVerificationMethod.MANDATORY:
                email_address = user.emailaddress_set.get(email=user.email)
                if not email_address.verified:
                    raise serializers.ValidationError(_('E-mail is not verified.'))

        attrs['user'] = user
        return attrs


class UserSerializer(serializers.ModelSerializer):
    skills = SkillSerializer(many=True, read_only=True)
    skill_ids = serializers.ListField(child=serializers.IntegerField(), write_only=True)
    password = serializers.CharField(write_only=True, style={'input_type': 'password'}, required=False)
    group_ids = serializers.ListField(child=serializers.IntegerField(), write_only=True)

    class Meta:
        model = User
        fields = ('id', 'email', 'first_name', 'last_name', 'introduction', 'profession',
                  'skills', 'phone',
                  'website', 'created_at', 'updated_at',
                  'password', 'skill_ids', 'group_ids',
                  'groups'
                  )
        read_only_fields = ('groups', 'created_at', 'updated_at', 'profile_image')

    @staticmethod
    def add_group(user, gid):
        group_name = {
            '1': 'offering',
            '2': 'seeking',
        }[str(gid)]
        group, _ = Group.objects.get_or_create(name=group_name)
        user.groups.add(group)

    def create(self, validated_data):
        model_class = self.Meta.model
        skill_ids = validated_data.pop('skill_ids', None)
        group_ids = validated_data.pop('group_ids', None)

        email = validated_data.pop('email')
        password = validated_data.pop('password')

        instance = model_class.objects.create_user(email=email, password=password)

        for (key, value) in validated_data.items():
            setattr(instance, key, value)
        instance.save()

        if group_ids:
            for gid in group_ids:
                self.add_group(instance, gid)

        if skill_ids:
            for sid in skill_ids:
                try:
                    instance.skills.add(Skill.objects.get(id=sid))
                except Exception as e:
                    pass

        return instance

    def update(self, instance, validated_data):
        skill_ids = validated_data.pop('skill_ids', None)
        group_ids = validated_data.pop('group_ids', None)

        super(UserSerializer, self).update(instance, validated_data)

        if skill_ids:
            instance.skills.clear()
            for sid in skill_ids:
                try:
                    instance.skills.add(Skill.objects.get(id=sid))
                except Exception as e:
                    pass

        if group_ids:
            instance.groups.clear()
            for gid in group_ids:
                self.add_group(instance, gid)

        return instance


class ProfileImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('profile_image', )

    def create(self, validated_data):
        raise NotImplementedError

    def update(self, instance, validated_data):
        super(ProfileImageSerializer, self).update(instance, validated_data)
        return instance
