# -*- coding: utf-8 -*-

from django.db import models
from django.conf import settings


class Kit(models.Model):

    """
    @note: 游记
    """
    user_id = models.CharField(max_length=32, db_index=True)
    title = models.CharField(max_length=128)
    content = models.TextField()
    views_count = models.IntegerField(default=0)
    answer_count = models.IntegerField(default=0)
    last_answer_time = models.DateTimeField(db_index=True)
    sort_num = models.IntegerField(default=0, db_index=True)
    like_count = models.IntegerField(default=0)
    is_important = models.BooleanField(default=False)   # 是否是精华帖
    is_silence = models.BooleanField(default=False, db_index=True)   # 是否静默，部分话题下的提问采取静默模式，不发feed，不在全部信息中展示
    ip = models.CharField(max_length=32, null=True)
    is_hide_user = models.BooleanField(default=False)
    state = models.BooleanField(default=True, db_index=True)
    create_time = models.DateTimeField(db_index=True, auto_now_add=True)

    class Meta:
        ordering = ["-sort_num",  "-create_time"]

    def get_url(self):
        return u'/kit/%s' % self.id

    def get_summary(self):
        """
        @attention: 通过内容获取摘要
        """
        from common import utils
        return utils.get_summary_from_html_by_sub(self.content)

    def get_user(self):
        from www.account.interface import UserBase
        return UserBase().get_user_by_id(self.user_id)

    def get_cover(self):
        import re

        tag_img = re.compile('<img .*?src=[\"\'](.+?)[\"\']')
        imgs = tag_img.findall(self.content)
        if imgs:
            return imgs[0]
        return '%s/img/default_kit_cover.jpg' % settings.MEDIA_URL
