from django.db import models

class CodeSample(models.Model):
    """The dataset: curated beginner code snippets with reference explanations."""
    title = models.CharField(max_length=200)
    language = models.CharField(max_length=30, default="python")
    difficulty = models.CharField(max_length=20, default="beginner")
    code = models.TextField()
    reference_explanation = models.TextField()

    def __str__(self):
        return self.title

class ExplanationLog(models.Model):
    """Every request the tool serves, which also grows into a dataset."""
    language = models.CharField(max_length=30)
    code = models.TextField()
    explanation = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]