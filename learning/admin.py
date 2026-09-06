from django.contrib import admin

from .models import LearningPath, Lesson


class LessonInline(admin.TabularInline):
    model = Lesson
    fields = (
        "title",
        "difficulty",
        "reading_time",
        "order",
        "is_published",
    )
    extra = 0
    show_change_link = True
    ordering = ("order",)


@admin.register(LearningPath)
class LearningPathAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "order",
        "is_published",
        "lesson_count",
    )
    list_editable = (
        "order",
        "is_published",
    )
    list_filter = ("is_published",)
    search_fields = (
        "title",
        "description",
    )
    prepopulated_fields = {
        "slug": ("title",),
    }
    ordering = (
        "order",
        "title",
    )
    inlines = [LessonInline]

    @admin.display(description="Quantidade de aulas")
    def lesson_count(self, learning_path):
        return learning_path.lessons.count()


@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "learning_path",
        "difficulty",
        "reading_time",
        "order",
        "is_published",
    )
    list_editable = (
        "order",
        "is_published",
    )
    list_filter = (
        "is_published",
        "difficulty",
        "learning_path",
    )
    search_fields = (
        "title",
        "summary",
        "content",
    )
    prepopulated_fields = {
        "slug": ("title",),
    }
    filter_horizontal = (
        "cocktails",
        "techniques",
    )
    ordering = (
        "learning_path",
        "order",
        "title",
    )
    list_select_related = ("learning_path",)

    fieldsets = (
        (
            "Informações principais",
            {
                "fields": (
                    "learning_path",
                    "title",
                    "slug",
                    "summary",
                    "content",
                )
            },
        ),
        (
            "Organização",
            {
                "fields": (
                    "difficulty",
                    "reading_time",
                    "order",
                    "is_published",
                )
            },
        ),
        (
            "Conteúdo relacionado",
            {
                "fields": (
                    "cocktails",
                    "techniques",
                ),
                "classes": ("collapse",),
            },
        ),
    )
