from django.db import models
from .enums import ACTOR_TYPE, TARGET_TYPE

class InteractionBase(models.Model):
    """
    مدل پایه برای تمام تعاملات
    """
    actor_type = models.CharField(max_length=20, choices=ACTOR_TYPE, db_index=True, verbose_name='نوع عملگر')
    actor_id = models.CharField(max_length=10, db_index=True, verbose_name='شناسه عملگر')
    
    target_type = models.CharField(max_length=20, choices=TARGET_TYPE, db_index=True, verbose_name='نوع هدف')
    target_id = models.CharField(max_length=10, db_index=True, verbose_name='شناسه هدف')
    
    created_at = models.DateTimeField(auto_now_add=True, db_index=True, verbose_name='تاریخ ایجاد')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='تاریخ بروزرسانی')
    
    metadata = models.JSONField(default=dict,blank=True,verbose_name='اطلاعات اضافی')
    
    class Meta:
        abstract = True
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.actor_type}:{self.actor_id} -> {self.target_type}:{self.target_id}"
