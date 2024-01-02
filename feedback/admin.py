from django.contrib import admin
from .models import FeedbackRound
from django.utils import timezone


@admin.register(FeedbackRound)
class FeedbackRoundAdmin(admin.ModelAdmin):
    list_display = ('employer', 'name', 'start_time', 'feedback_round_code', 'feedback_send_window_end', 'data_retention_end_time')
    list_filter = ('employer', )
    search_fields = ('name', 'employer__email')

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.filter(feedback_send_window_end__gte=timezone.now())
