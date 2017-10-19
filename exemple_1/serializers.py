from rest_framework import serializers
from api.models import Token
from nc_accounts.models import account, Account


class TokenSerializer(serializers.ModelSerializer):
    class Meta:
        model = Token
        fields = ('id', 'platform', 'user_agent')


class AccountCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = account
        fields = (
            'id',
            'email',
            'birthday',
            'legal_person',
            'first_name',
            'last_name',
            'middle_name',
            'full_name',
        )
        extra_kwargs = {
            'full_name': {'read_only': True, 'source': 'get_full_name'},
            'email': {'read_only': True, 'source': 'get_email'}
        }


class AccountDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = (
            'id',
            'birthday',
            'legal_person',
            'first_name',
            'last_name',
            'middle_name',

        )


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()


class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)
    retype_password = serializers.CharField(required=True)
