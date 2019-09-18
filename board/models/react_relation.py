from django.db import models
from django.contrib.auth.models import User
from board.models.card import Card
from utils.models import TimestampedModel
from model_utils import Choices




class Profile(TimestampedModel):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    react = models.ManyToManyField(
        Card,
        through='ReactRelation',
        related_name='react_relation',
        Symmetrical=False
    )

    def reaction_change(self, card):
        reactions, is_reactions = ReactRelation.objects.get_or_create(
            profile=self,
            card=card
        )
        if not is_reactions:
            reactions.delete()
        else:
            return reactions

    def like_counts(self):
        return ReactRelation.objects.filter(reaction_choice='like').count()

    def dislike_counts(self):
        return ReactRelation.objects.filter(reaction_choice='dislike').count()

    def __str__(self):
        return self.user.username

    class Meta:
        db_table = 'profile_relation'
        verbose_name = 'profile_relation'
        verbose_name_plural = '{} {}'.format(verbose_name, '목록')

choice = Choices(
    'like',
    'dislike'
)
class ReactRelation(TimestampedModel):
    card = models.ForeignKey(Card,
                             on_delete=models.CASCADE,
                             related_name='react_relations'
                             )



    profile = models.ForeignKey(Profile,
                             on_delete=models.CASCADE,
                             related_name='react_relations'
                                )

    reaction_choice = models.CharField(
        verbose_name="reaction_choice",
        choices=choice
    )

    def __str__(self):
        return f'{self.profile.user.username} like {self.card.title}'


    class Meta:
        db_table = 'card_relation'
        verbose_name = 'card_relation'
        verbose_name_plural = '{} {}'.format(verbose_name, '목록')

    # - 이 친구는 사용자가 카드에 대한 반응 Relation 모델입니다
    # - 특정 사용자가 특정 카드에 할 수 있는 반응(좋아요, 싫어요 등)에 대한 정보를 포함합니다.
    # - 특정 사용자가 특정 카드를 좋아한다/싫어한다 등의 관계 표현이 가능해야 합니다.
    # - 이 관계는 어떤 특정 유저의 반응이 반응인지에 대한 구별이 가능해야 합니다.
    #     - https://docs.djangoproject.com/en/2.1/ref/models/fields/#choices 를 참조하세요.
    # - django-model-utils 의 Choices 는 위 기능을 더욱 편리하게 사용할 수 있도록 도와줍니다. 사용하시길 추천드립니다.
    #     - 사용시에는 https://django-model-utils.readthedocs.io/en/latest/utilities.html#choices 를 참조하세요.
