from django.contrib import admin
from .models import FeedbackRound, Feedback
from django.utils import timezone


class FeedbackInline(admin.TabularInline):
    model = Feedback
    extra = 0  # !!!Prevents displaying extra empty forms
    fields = ['author', 'receiver', 'is_draft', 'created_at', 'updated_at']
    readonly_fields = ['created_at', 'updated_at']


@admin.register(FeedbackRound)
class FeedbackRoundAdmin(admin.ModelAdmin):
    list_display = ('employer', 'name', 'start_time', 'feedback_round_code', 'feedback_send_window_end', 'data_retention_end_time')
    list_filter = ('employer', )
    search_fields = ('name', 'employer__email')
    inlines = [FeedbackInline]

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.filter(feedback_send_window_end__gte=timezone.now())

@admin.register(Feedback)
class FeedbackAdmin(admin.ModelAdmin):
    list_display = ('round', 'author', 'is_draft', 'created_at', 'updated_at')
    list_filter = ('is_draft', 'round', 'author')
    search_fields = ('content', 'round__name', 'author__username')

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.order_by('-updated_at')