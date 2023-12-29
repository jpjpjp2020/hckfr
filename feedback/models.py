from django.db import models
import uuid
from entry.views import User
from datetime import timedelta
from django.utils import timezone
from .constants import DEFAULT_FEEDBACK_WINDOW, DEFAULT_DATA_RETENTION_PERIOD


# basis for extensions and user feature RBAC logic
# When initializing a new FeedbackRound, 1 option:
# feedback_window = specific_feedback_window or GlobalSettings.objects.get(name="default_feedback_window").value

class GlobalSettings(models.Model):
    glbal_feedback_send_window_end = models.IntegerField(default=DEFAULT_FEEDBACK_WINDOW)
    global_data_retention_end_time = models.IntegerField(default=DEFAULT_DATA_RETENTION_PERIOD)
   

class FeedbackRound(models.Model):
    employer = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=150)
    start_time = models.DateTimeField(auto_now_add=True)
    feedback_round_code = models.CharField(max_length=25, default=uuid.uuid4, unique=True)
    feedback_send_window_end = models.DateTimeField(default=lambda: timezone.now() + timedelta(days=DEFAULT_FEEDBACK_WINDOW))
    data_retention_end_time = models.DateTimeField(default=lambda: timezone.now() + timedelta(days=DEFAULT_DATA_RETENTION_PERIOD))

    @classmethod
    def can_initiate_new_round(cls, employer_id):
        return not cls.objects.filter(employer_id=employer_id, feedback_send_window_end__gt=timezone.now()).exists()

    def save(self, *args, **kwargs):
        # Placeholder for is_active status or other needed business logic
        super().save(*args, **kwargs)


class Feedback(models.Model):
    round = models.ForeignKey(FeedbackRound, on_delete=models.CASCADE)
    sender = models.ForeignKey(User, related_name='sent_feedback', on_delete=models.CASCADE)
    receiver = models.ForeignKey(User, related_name='received_feedback', on_delete=models.CASCADE)
    title = models.CharField(max_length=150)
    content = models.TextField()
    is_draft = models.BooleanField(default=True)

    # encryption placeholder
    def encrypt_feedback(self):
        # logic placeholder
        pass

