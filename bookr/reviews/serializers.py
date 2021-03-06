from rest_framework import serializers
from .models import Contributor,Book,Publisher,BookContributor,Contributor
# class PublisherSerializer(serializers.Serializer):
#     name=serializers.CharField()
#     website=serializers.URLField()
#     email=serializers.EmailField()
# class BookSerializer(serializers.Serializer):
#     title=serializers.CharField()
#     publication_date=serializers.DateField()
#     isbn=serializers.CharField()
#     publisher=PublisherSerializer()

class ContributorSerializer(serializers.ModelSerializer):
    class Meta:
        model=Contributor
        fields=['first_names','last_names','email']
class PublisherSerializer(serializers.ModelSerializer):
    class Meta:
        model=Publisher
        fields=['name','website','email']
class BookSerializer(serializers.ModelSerializer):
    publisher=PublisherSerializer()
    class Meta:
        model=Book
        fields=['title','publication_date','isbn','publisher']

class ContributionSerializer(serializers.ModelSerializer):
    book=BookSerializer()
    class Meta:
        model=BookContributor
        fields=['book','role']
class ContributorSerializer(serializers.ModelSerializer):
    bookcontributor_set=ContributionSerializer(read_only=True,many=True)
    number_contributions=serializers.ReadOnlyField()
    class Meta:
        model=Contributor
        fields=['first_names','last_names','email','bookcontributor_set','number_contributions']