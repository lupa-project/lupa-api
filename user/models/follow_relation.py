from django.db import models

from utils.models import TimestampedModel
from django.contrib.auth.models import User


class UserAccount(TimestampedModel):
    user = models.OneToOneField(
        # User 테이블을 구조적으로 확장
        User,
        on_delete=models.CASCADE
    )

    follows = models.ManyToManyField(
        # UserAccount 자기 자신의 모델과 N:N 관계
        'self',
        # 비대칭 관계
        symmetrical=False,
        # 중개 모델
        through='FollowRelation'
    )

    def __str__(self):
        return self.user.username

    def follow(self, to_user):
        return

    def unfollow(self, to_user):
        return

    def get_following(self):
        # 내가 follow 하고 있는 UserAccount 목록 가져오기
        return

    def get_followers(self):
        # 나를 follow 하고 있는 UserAccount 목록 가져오기
        return

    class Meta:
        db_table = 'user_account'
        verbose_name = 'User Account'
        verbose_name_plural = '{} {}'.format(verbose_name, '목록')


class FollowRelation(TimestampedModel):
    # - 이 친구가 이제 FollowRelation 모델입니다.
    # - `UserA 가 UserB 를 팔로우하다` 대한 정의가 가능해야 합니다.
    # - User 모델은 `django.contrib.auth.models.User` 를 사용하시면 됩니다.
    # - 만들어지는 모델은 다음과 같은 표현이 가능해야합니다.
    #     - `UserA 는 UserB 를 팔로우하였으며, 아직 승인되지 않았다 / 승인되었다`
    follower = models.ForeignKey(
        UserAccount,
        on_delete=models.CASCADE,
        related_name='followers'
    )
    following = models.ForeignKey(
        UserAccount,
        on_delete=models.CASCADE,
        related_name='followings'
    )

    def __str__(self):
        return f'{self.follower.user.username} -> {self.following.user.username}'

    def approval(self, to_user):
        return

    class Meta:
        db_table = 'follow_relation'
        verbose_name = 'Follow Relation'
        verbose_name_plural = '{} {}'.format(verbose_name, '목록')
