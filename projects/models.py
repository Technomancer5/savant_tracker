from django.db import models

class Project(models.Model):
    name = models.CharField(max_length=255, verbose_name="Project / Topic")
    category = models.CharField(max_length=100, blank=True, null=True)
    project_type = models.CharField(max_length=100, blank=True, null=True, verbose_name="Type")
    priority = models.CharField(max_length=50, blank=True, null=True)
    status = models.CharField(max_length=50, blank=True, null=True)
    last_updated = models.DateField(blank=True, null=True)
    summary = models.TextField(blank=True, null=True)
    links = models.TextField(blank=True, null=True, help_text="Main File / Notes Links")
    
    # New columns added to match original spreadsheet exactly!
    ai_source = models.CharField(max_length=255, blank=True, null=True, verbose_name="AI Source")
    ai_prompt_link = models.TextField(blank=True, null=True, verbose_name="AI Prompt Link")
    related_websites = models.TextField(blank=True, null=True, verbose_name="Related Websites")
    
    tags = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return self.name

class StudyLog(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='logs')
    date_logged = models.DateTimeField(auto_now_add=True)
    duration_minutes = models.IntegerField(help_text="Time spent in minutes")
    notes = models.TextField()

    def __str__(self):
        return f"{self.project.name} - {self.date_logged.strftime('%Y-%m-%d')}"