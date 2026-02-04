from django.db import models

# Create your models here.

class Kana(models.Model):
    HIRAGANA = 'hira'
    KATAKANA = 'kata'
    KANA_TYPE_CHOICES = [
        (HIRAGANA, '平假名'),
        (KATAKANA, '片假名'),
    ]
    
    hiragana = models.CharField(max_length=2, verbose_name='平假名')
    katakana = models.CharField(max_length=2, verbose_name='片假名')
    romaji = models.CharField(max_length=10, verbose_name='罗马音')
    kana_type = models.CharField(max_length=4, choices=KANA_TYPE_CHOICES, default=HIRAGANA, verbose_name='假名类型')
    
    class Meta:
        verbose_name = '假名'
        verbose_name_plural = '假名表'
        ordering = ['id']
    
    def __str__(self):
        return f'{self.hiragana}({self.katakana}) - {self.romaji}'

class UserProgress(models.Model):
    user_id = models.IntegerField(verbose_name='用户ID')
    kana = models.ForeignKey(Kana, on_delete=models.CASCADE, verbose_name='假名')
    correct_count = models.IntegerField(default=0, verbose_name='正确次数')
    wrong_count = models.IntegerField(default=0, verbose_name='错误次数')
    last_practiced = models.DateTimeField(auto_now=True, verbose_name='最后练习时间')
    
    class Meta:
        verbose_name = '用户进度'
        verbose_name_plural = '用户进度表'
        unique_together = ['user_id', 'kana']
        ordering = ['-last_practiced']
    
    def __str__(self):
        return f'用户{self.user_id} - {self.kana}'
    
    @property
    def total_attempts(self):
        return self.correct_count + self.wrong_count
    
    @property
    def accuracy_rate(self):
        if self.total_attempts == 0:
            return 0
        return round((self.correct_count / self.total_attempts) * 100, 2)
