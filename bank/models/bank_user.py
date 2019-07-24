from django.db import models


class BankUser(models.Model):
    id = models.AutoField(primary_key=True)
    seq_no = models.CharField(verbose_name="사용자일련번호", max_length=10,
                              null=False, blank=False, help_text="은행 Api 에서 주는 유저의 식별 번호")
    connect_info = models.CharField(verbose_name="bank_connect_info", max_length=4000,
                                    null=False, blank=False, help_text="은행 Api 에서 주는 유저 연결 정보")
    user_name = models.CharField(verbose_name="오픈플랫폼고객실명", max_length=20,
                                 null=False, blank=False, help_text="은행 Api 에서 주는 유저 연결 정보")
    access_token = models.CharField(verbose_name="사용자token", max_length=255,
                                    null=False, blank=False, help_text="은행 Api 사용자 인증용 token")
    refresh_token = models.CharField(verbose_name="사용자갱신용token", max_length=255,
                                     null=False, blank=False, help_text="은행 Api 사용자 인증용 토큰을 갱신하기 위한 token")
    scope = models.CharField(verbose_name="오픈플랫폼고객실명", max_length=25,
                             null=False, blank=False, help_text="은행 Api 에서 주는 유저 연결 정보")
    expire_time = models.IntegerField(verbose_name="토큰만료시간")
    create_time = models.DateTimeField(auto_now_add=True)
    update_time = models.DateTimeField(auto_now=True)
