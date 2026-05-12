from rest_framework import serializers
from .models import Category, Candidate, Vote, ElectionResult, VoteBlock


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class CandidateSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source='category.name', read_only=True)
    voting_start = serializers.DateField(source='category.start_date', read_only=True)
    voting_end = serializers.DateField(source='category.end_date', read_only=True)
    votes = serializers.SerializerMethodField()
    policies = serializers.SerializerMethodField()
    profile_image = serializers.SerializerMethodField()  # Updated

    class Meta:
        model = Candidate
        fields = [
            'id', 'name', 'category', 'category_name',
            'bio', 'policy', 'profile_image',
            'voting_start', 'voting_end', 'votes', 'policies'
        ]

    def get_profile_image(self, obj):
        """Return full URL for profile image"""
        if obj.profile_image:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(obj.profile_image.url)
            return obj.profile_image.url
        return None

    def get_votes(self, obj):
        return obj.votes.count()

    def get_policies(self, obj):
        if not obj.policy:
            return []
        lines = [l.strip() for l in obj.policy.strip().split('\n') if l.strip()]
        policies = []
        i = 0
        while i < len(lines):
            title = lines[i]
            desc = lines[i + 1] if i + 1 < len(lines) else ""
            policies.append({"title": title, "desc": desc})
            i += 2
        return policies


class VoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vote
        fields = ['id', 'candidate', 'voter', 'timestamp', 'block_hash']
        read_only_fields = ['voter', 'timestamp', 'block_hash']


class ElectionResultSerializer(serializers.ModelSerializer):
    candidate_name = serializers.CharField(source='candidate.name', read_only=True)
    category_name = serializers.CharField(source='category.name', read_only=True)
    profile_image = serializers.SerializerMethodField()  # Updated

    class Meta:
        model = ElectionResult
        fields = ['id', 'category', 'category_name', 'candidate', 'candidate_name', 'vote_count', 'profile_image']

    def get_profile_image(self, obj):
        """Return full URL for profile image"""
        if obj.candidate.profile_image:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(obj.candidate.profile_image.url)
            return obj.candidate.profile_image.url
        return None

class VoteBlockSerializer(serializers.ModelSerializer):
    class Meta:
        model = VoteBlock
        fields = '__all__'
