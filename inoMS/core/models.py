from django.db import models

# Create your models here.
""" ************************* Language **************************************************************************** """

# class Language(models.Model):
#     english_name = models.CharField(verbose_name='english name', max_length=60, unique=True)
#     abbreviation = models.CharField(verbose_name='abbreviation', max_length=3, unique=True)
#
#     # translation_objs = JSONField(default=dict)
#     translation_objs = models.ManyToManyField(to='LanguageTranslation', blank=True, related_name="language_tr")
#
#     class Meta:
#         db_table = 'language'
#
#
# class LanguageTranslation(models.Model):
#     language = models.ForeignKey('Language', models.CASCADE, help_text='please enter language id',
#                                  related_name='language')
#     language_2 = models.ForeignKey('Language', models.CASCADE, help_text='please enter language id 2',
#                                    related_name='language_2')
#     name = models.CharField(verbose_name='name', max_length=60, unique=True,
#                             help_text='please enter language translated name')
#
#     class Meta:
#         db_table = 'language_translation'
#         # unique_together = ('language', 'language_2', 'name')
