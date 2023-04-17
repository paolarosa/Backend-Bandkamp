from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from .models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username", "email", "password", "first_name", "last_name", "is_superuser"]
        ready_only_fields = ["is_superuser"]
        extra_kwargs = {
            "username":{
                "validators":[
                    UniqueValidator(
                        queryset=User.objects.all(),
                        message="A user with that username already exists.",
                    )
                ]
            },
            "email":{
                "validators": [
                    UniqueValidator(queryset=User.objects.all())],
                "required": True,
            },
            "password": {"write_only": True}
        }
    

    def create(self, validated_data: dict) -> User:
        return User.objects.create_superuser(**validated_data)

    def update(self, instance: User, validated_data: dict) -> User:
        password = validated_data.get("password", None)
        if password:
            validated_data.pop("password")
            instance.set_password(password)
        for key, value in validated_data.items():
            setattr(instance, key, value)

        instance.save()

        return instance
