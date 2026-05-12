from django.contrib import admin
from .models import Category, Candidate, Vote, ElectionResult, VoteBlock


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'start_date', 'end_date']


@admin.register(Candidate)
class CandidateAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'profile_image']
    list_filter = ['category']
    search_fields = ['name']
    fields = ['name', 'category', 'bio', 'policy', 'profile_image']


@admin.register(Vote)
class VoteAdmin(admin.ModelAdmin):
    list_display = ['voter', 'candidate', 'timestamp', 'block_hash']


@admin.register(ElectionResult)
class ElectionResultAdmin(admin.ModelAdmin):
    list_display = ['category', 'candidate', 'vote_count']


@admin.register(VoteBlock)
class VoteBlockAdmin(admin.ModelAdmin):
    list_display = ['index', 'timestamp', 'hash', 'previous_hash']
    readonly_fields = ['index', 'timestamp', 'data', 'previous_hash', 'hash']