from django.contrib import admin

from .models import AnalysisResult, AdminTable


class AnalysisResultAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "text",
        "user_type",
        "user_category",
        "user_location",
        "analyzed_text",
        "improved_text",
        "reference_urls",
    )
    actions = ["send_to_admin"]

    def send_to_admin(self, request, queryset):
        selected_records = queryset.values("text", "analyzed_text")

        for record in selected_records:
            AdminTable.objects.create(
                question=record["text"], analyzed_answer=record["analyzed_text"]
            )

        self.message_user(request, "New table created with selected rows.")

    send_to_admin.short_description = "Send question and answer to admin table"


admin.site.register(AnalysisResult, AnalysisResultAdmin)
admin.site.register(AdminTable)
