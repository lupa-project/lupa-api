from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import permission_classes
from rest_framework.permissions import AllowAny
from bank.request.auth import (
    get_bank_user_info,
    get_token,
)
from bank.models import (
    BankAccount,
    BankUser,
)
import datetime


@permission_classes(AllowAny)
class CreateBankUserCallBack(APIView):

    def validate_data(self, authorization_code, scope):
        return not (
            isinstance(authorization_code, str)
            and isinstance(scope, str)
        )

    def get(self, request):
        authorization_code = request.query_params.get('code', None)
        scope = request.query_params.get('scope', None)
        client_info = request.query_params.get('client_info', None)

        if self.validate_data(authorization_code=authorization_code, scope=scope):
            # TODO logger setting 이후 error logging 필요함
            raise ValueError
        res = get_token(code=authorization_code)
        access_token = res['access_token']
        token_type = res['token_type']
        expires_in = res['expires_in']
        refresh_token = res['refresh_token']
        scope = res['scope']
        user_seq_no = res['user_seq_no']

        res = get_bank_user_info(token=access_token, user_seq_no=user_seq_no)

        api_tran_id = res['api_tran_id']
        rsp_code = res['rsp_code']
        rsp_message = res['rsp_message']
        api_tran_dtm = res['api_tran_dtm']
        user_seq_no = res['user_seq_no']
        user_ci = res['user_ci']
        user_name = res['user_name']
        res_cnt = res['res_cnt']
        account_list = res['res_list']

        bank_user = BankUser.objects.create(
            seq_no=user_seq_no,
            connect_info=user_ci,
            user_name=user_name,
            access_token=access_token,
            refresh_token=refresh_token,
            scope=scope,
            expire_time=datetime.datetime.now() + datetime.timedelta(seconds=expires_in)
        )

        bulk_account_create_list = []
        for account in account_list:
            fintech_use_num = account['fintech_use_num']
            account_alias = account['account_alias']
            bank_code_std = account['bank_code_std']
            bank_code_sub = account['bank_code_sub']
            bank_name = account['bank_name']
            account_num_masked = account['account_num_masked']
            account_holder_name = account['account_holder_name']
            account_type = account['account_type']
            inquiry_agree_yn = account['inquiry_agree_yn']
            inquiry_agree_dtime = account['inquiry_agree_dtime']
            transfer_agree_yn = account['transfer_agree_yn']
            transfer_agree_agreement = transfer_agree_yn if transfer_agree_yn != "" else None
            transfer_agree_dtime = account['transfer_agree_dtime']
            transfer_agree_datetime = (datetime.datetime.strptime(transfer_agree_dtime, '%Y%m%d%H%M%S')
                                       if transfer_agree_dtime != "" else None)
            bulk_account_create_list.append(
                BankAccount(
                    bank_user=bank_user,
                    fintech_use_num=fintech_use_num,
                    account_alias=account_alias,
                    bank_code_std=bank_code_std,
                    bank_code_sub=bank_code_sub,
                    account_num_masked=account_num_masked,
                    account_holder_name=account_holder_name,
                    account_type=account_type,
                    inquiry_agreement=inquiry_agree_yn,
                    inquiry_agree_datetime=datetime.datetime.strptime(inquiry_agree_dtime, '%Y%m%d%H%M%S'),
                    transfer_agreement=transfer_agree_agreement,
                    transfer_agree_datetime=transfer_agree_datetime,
                )
            )
        BankAccount.objects.bulk_create(bulk_account_create_list)

        response_data = {
            'bank_user': bank_user.pk
        }
        return Response(status=200, data=response_data)
