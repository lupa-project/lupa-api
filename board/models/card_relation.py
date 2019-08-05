from django.db import models

from utils.models import TimestampedModel


class CardRelation(TimestampedModel):
    # - 이 친구가 이제 카드 Relation 모델입니다
    # - 카드 A 로부터 카드 B 가 어떤 관계를 가지는지에 대한 정의가 가능해야 합니다.
    # - 만들어지는 모델은 다음과 같은 표현이 가능해야합니다.
    #     - 1. 카드 A 는 카드 B 의 하위 카드이다.
    #     - 2. 카드 C 는 카드 B 의 댓글 카드이다.
    # - 이 관계는 어떤 관계인지에 대한 구별이 가능해야 합니다.
    #     - https://docs.djangoproject.com/en/2.1/ref/models/fields/#choices 를 참조하세요.
    # - django-model-utils 의 Choices 는 위 기능을 더욱 편리하게 사용할 수 있도록 도와줍니다. 사용하시길 추천드립니다.
    #     - 사용시에는 https://django-model-utils.readthedocs.io/en/latest/utilities.html#choices 를 참조하세요.

    class Meta:
        db_table = 'card_relation'
        verbose_name = '카드 Relation'
        verbose_name_plural = '{} {}'.format(verbose_name, '목록')
