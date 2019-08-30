from django.db import models
from bank.models import BankUser


class BankAccount(models.Model):
    id = models.AutoField(primary_key=True)
    bank_user = models.ForeignKey(to=BankUser, on_delete=models.CASCADE, verbose_name="은행사용자정보",
                                  null=False, related_name="bank_account_for_bank_user", db_constraint=False)
    fintech_use_num = models.CharField(verbose_name="핀테크이용번호", max_length=25,
                              null=False, blank=False)
    account_alias = models.CharField(verbose_name="계좌별명", max_length=50,
                                    null=False, blank=False, help_text="유저가 회원가입시 기입한 계좌 별명")
    bank_code_std = models.CharField(verbose_name="은행표준코드", max_length=3,
                                 null=False, blank=False, help_text="3자리 은행 코드")
    bank_code_sub = models.CharField(verbose_name="은행점별코드", max_length=7,
                                    null=False, blank=False, help_text="출금/개설 기관 점별 코드")
    # TODO 실제 은행 계좌 번호는 사업자 등록 후 Api 심사 통과하면 사용할 수 있음. 그 전 까지는 마스킹된 계좌번호만 받을 수 있음.
    account_num = models.CharField(verbose_name="계좌번호", max_length=20,
                                          null=True, blank=True, help_text="계좌번호-사업자등록이후사용가능")
    account_num_masked = models.CharField(verbose_name="마스킹된게좌번호", max_length=20,
                                        null=False, blank=False, help_text="뒷자리가 마스킹된 계좌번호")
    account_holder_name = models.CharField(verbose_name="계좌입금주명", max_length=20,
                             null=False, blank=False, help_text="계좌주의 실명")
    account_type = models.CharField(verbose_name="계좌구분", max_length=1,
                                           null=False, blank=False, help_text="개인 계좌인지 아닌지 파악용")
    inquiry_agreement = models.CharField(verbose_name="조회서비스동의여부", max_length=1,
                                           null=False, blank=False, help_text="금융오픈플랫폼(오픈뱅킹) 계좌조회 동의여부")
    inquiry_agree_datetime = models.DateTimeField(verbose_name="조회서비스동의날짜", null=True, blank=True)

    transfer_agreement = models.CharField(verbose_name="오픈플랫폼고객실명", max_length=25,
                                          null=True, blank=False, help_text="은행 Api 에서 주는 유저 연결 정보")
    transfer_agree_datetime = models.DateTimeField(verbose_name="출금서비스동의날짜", null=True, blank=True)

    create_time = models.DateTimeField(auto_now_add=True)
    update_time = models.DateTimeField(auto_now=True)

    def __str__(self):
        return 'id: {}'.format(self.id)

    class Meta:
        db_table = 'bank_account'
        verbose_name = '은행 유저 정보'
        verbose_name_plural = verbose_name