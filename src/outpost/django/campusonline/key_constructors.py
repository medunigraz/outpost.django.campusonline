from outpost.django.base.key_constructors import AuthenticatedKeyBit
from rest_framework_extensions.key_constructor import bits
from rest_framework_extensions.key_constructor.constructors import DefaultKeyConstructor


class PersonKeyConstructor(DefaultKeyConstructor):
    authenticated = AuthenticatedKeyBit()
    unique_view_id = bits.UniqueMethodIdKeyBit()
    format = bits.FormatKeyBit()
    route = bits.QueryParamsKeyBit()


class DistributionListKeyConstructor(DefaultKeyConstructor):
    authenticated = AuthenticatedKeyBit()
    unique_view_id = bits.UniqueMethodIdKeyBit()
    format = bits.FormatKeyBit()
    route = bits.QueryParamsKeyBit()
