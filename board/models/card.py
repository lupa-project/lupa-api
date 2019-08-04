from django.db import models
# 장고에서 기본적으로 지원해주는 User 모델입니다. Password Validation, Permission 등 여러 유틸을 지원합니다.
# LUPA 에서 Root 격 되는 유저 모델은 이것을 사용할 생각입니다.
from django.contrib.auth.models import User


class Card(models.Model):
    # ForeignKey 는 타 모델과의 관계를 정의하는 필드입니다.
    # 아래와 같이 정의한 경우, User 가 여러 Board 를 가지는 1:N 관계가 성립됩니다.
    # 이렇게 만들어진 필드는 DB 상에서는 <필드이름>_id (아래의 경우 `user_id`) 로 생성되며,
    # `to` 에 지정한 모델의 Primary key 를 값으로 저장하게 됩니다.

    # id = models.AutoField(primary_key=True)
    # 장고에서, PrimaryKey 는 정의해줄 수 있으나 직접 정의하지 않은 경우 `id` 란 이름으로 자동 생성해줍니다.
    # 따라서 추가적인 커스터마이징이 필요하지 않은 경우, 정의해주지 않습니다.

    # Django 에서는 ForeignKey 에 대해 Directly referencing 할 수 있습니다.
    # 특정 Card 인스턴스를 작성한 User 의 email 에 접근하고 싶다면 `card.user.email` 과 같은 형태로 접근할 수 있습니다.
    user = models.ForeignKey(
        # `to` 필드는 관계의 대상이 되는 모델을 지정해줍니다.
        to=User,
        # `on_delete` 옵션은 이 필드와 관계를 가지는 모델(여기서는 User)의 row 가 DB 상에서 삭제될 때,
        # 그 row 의 primary key 를 foreign key 로 가지는 타 모델(여기서는 Card)의 row 를 어떻게 처리할지에 대한 정의입니다.
        # `CASCADE` 는 Board 를 User 에 종속적인 관계로 정의합니다. 즉, User 가 삭제되면 그에 해당하는 Card 도 따라 삭제됩니다.
        # 그 외에 `DO_NOTHING`, `SET_DEFAULT`, `SET_NULL` 등의 옵션이 있습니다. 필요에 따라 찾아보시면 될 것 같습니다.
        on_delete=models.CASCADE,
        # `related_name` 옵션은 관계의 대상이 되는 모델(여기서는 User)에서 이 모델(여기서는 Card)로 접근할 때 사용할 키워드를 정의합니다.
        # 여기서 지정된 키워드는 관계의 대상이 되는 모델(여기서는 User)의 인스턴스에서 Manager 를 사용하듯 접근할 수 있습니다.
        # 역참조 쿼리 시 사실상 필드 이름과 동일하게 사용되기 때문에 네이밍에 신중해야 합니다. 반드시 복수형으로 정의해주세요.
        # 특정 User 인스턴스가 가지고 있는 Card 를 모두 가져오고 싶다면 `user.cards.all()` 로 접근할 수 있습니다.
        related_name='cards',
        # `verbose_name` 은 이 필드의 readable 한 명칭을 정의합니다.
        # 여기서 정의된 필드 명칭은 후에 ModelForm, ModelAdmin 을 다룰 때 장고에서 사용하게 됩니다. (필드 라벨을 자동으로 만들어준다거나 등...)
        verbose_name='작성자',
        # 그 외에도 여러가지 가능한 옵션이 있습니다.
        # https://docs.djangoproject.com/en/2.1/ref/models/fields/#module-django.db.models.fields 를 참조해주세요.
    )

    # TODO: 아직 BankHistory(입출금내역) 모델이 만들어지지 않아, ForeignKey 를 걸 수 없으므로 주석처리합니다.
    """
    bank_history = models.ForeignKey(
        to=BankHistory,
        on_delete=models.CASCADE,
        related_name='cards',
        verbose_name='입출금내역',
    )
    """

    is_hidden = models.BooleanField(
        # 모델에 대해 DB 에 추가시 값을 지정해주지 않은 경우, 기본값으로 무엇을 사용할지에 대해 정의해줄 수 있습니다.
        default=False,
        verbose_name='숨김처리여부',
        # 도움말입니다. 실제 유저 인터페이스에 노출되지는 않고, 어드민 등에서 노출됩니다.
        help_text='숨김처리된 보드는 작성자에게만 노출됩니다.'
    )

    title = models.CharField(
        # CharField 와 같이 문자열 타입의 필드의 경우(TextField 제외) max_length 를 지정해주어야 합니다.
        max_length=255,
        verbose_name='타이틀',
    )

    content = models.TextField(
        verbose_name='내용',
        help_text='마크다운 에디터로 작성되어 마크다운 포맷으로 저장됩니다.',
    )

    created_datetime = models.DateTimeField(
        verbose_name='생성일시',
        # `auto_now_add` 옵션이 있을 경우, 모델 인스턴스가 처음으로 DB 에 생성될 때 장고에서 이 필드를 그 일시로 채워줍니다.
        auto_now_add=True,
    )

    updated_datetime = models.DateTimeField(
        verbose_name='수정일시',
        # `auto_now` 옵션이 있을 경우, 각각의 모델 인스턴스가 save 될 때마다 장고에서 이 필드를 그 일시로 업데이트 해줍니다.
        auto_now=True,
    )

    def __str__(self):
        # 만약 스트링 형태로 casting 시 어떤 형태로 보여줄지 정의합니다. (주로 django shell 을 이용한 command 처리시 보여집니다.)
        return f'Card(ID {self.id}, by {self.user}, at {self.created_datetime})'

    class Meta:
        # DB 상에서 사용할 테이블의 이름입니다.
        db_table = 'card'
        verbose_name = '카드'
        verbose_name_plural = '{} {}'.format(verbose_name, '목록')
