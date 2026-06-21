from django.contrib import admin
from core import models

# Register your models here.

""" ************************* Language **************************************************************************** """

# class LanguageAdmin(admin.ModelAdmin):
#     model = models.Language
#     list_display = ['id', 'english_name', 'abbreviation']
#     # exclude = ['english_name']
#     # list_display_links = ["id"]
#     # list_editable = ['english_name', 'abbreviation']
#     # search_fields = ['id', 'english_name', 'abbreviation']
#     # list_filter = ('create_time',)
#     # ordering = ('-create_time',)
#
#
# admin.site.register(models.Language, LanguageAdmin)
#
#
# class LanguageTranslationAdmin(admin.ModelAdmin):
#     model = models.LanguageTranslation
#     list_display = ['id', 'language_name', 'language_2', 'name']
#
#     def language_name(self, obj):
#         return obj.language.english_name
#
#
# admin.site.register(models.LanguageTranslation, LanguageTranslationAdmin)
