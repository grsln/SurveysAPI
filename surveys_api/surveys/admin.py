from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.safestring import mark_safe
from django.utils.translation import ugettext_lazy as _

from .models import Answer, Question, SimpleSurvey, SimpleSurveyResult, User, UserProfile


class UserProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser',
                                       'groups', 'user_permissions')}),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2'),
        }),
    )
    list_display = ('email', 'is_staff')
    search_fields = ('email',)
    ordering = ('email',)
    inlines = (UserProfileInline,)


class AnswerInline(admin.TabularInline):
    model = Answer
    extra = 1
    readonly_fields = ("get_image",)

    def get_image(self, obj):
        return mark_safe(f'<img src={obj.image.url} width="100" height="110"')

    get_image.short_description = "Изображение"


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    """Категории"""
    list_display = ("question", "image")
    inlines = [AnswerInline]
    save_on_top = True
    save_as = True
    # list_display_links = ("name",)


@admin.register(Answer)
class AnswerAdmin(admin.ModelAdmin):
    """Категории"""
    list_display = ("answer", "image", "id")
    # list_display_links = ("name",)


# admin.site.register(Question)
# admin.site.register(Answer)
admin.site.register(SimpleSurvey)
admin.site.register(SimpleSurveyResult)
admin.site.site_title = "Опросы"
admin.site.site_header = "Опросы"
