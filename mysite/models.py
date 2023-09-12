from django.db import models


class AnalysisResult(models.Model):
    text = models.TextField()
    user_type = models.CharField(max_length=100)
    user_category = models.CharField(max_length=100)
    user_location = models.CharField(max_length=100)
    analyzed_text = models.TextField()
    improved_text = models.TextField()
    reference_urls = models.JSONField(default=list)  # Corrected field name

    def __str__(self):
        return self.text


class AdminTable(models.Model):
    question = models.TextField()
    analyzed_answer = models.TextField()

    def __str__(self):
        return self.question
