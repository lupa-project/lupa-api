from django.db import models

from model_utils import Choices
from utils.models import TimestampedModel
from django.contrib.auth.models import User


class UserFollowInfo(TimestampedModel):
    user = models.OneToOneField(
        # User 테이블을 구조적으로 확장
        User,
        on_delete=models.CASCADE
    )

    follows = models.ManyToManyField(
        # UserFollowInfo 자기 자신의 모델과 N:N 관계
        'self',
        # 비대칭 관계
        symmetrical=False,
        # 중개 모델
        through='FollowRelation'
    )

    def __str__(self):
        return self.user.username

    def follow(self, to_user):
        """
        Create and Returns follow_info object

        Args:
            to_user (An instance of UserFollowInfo):

        Returns:
            An instance of FollowRelation or None
        """
        # Follow Relation 을 생성

        # get_or_create : 객체를 조회할 때 사용하는 메소드로 (object, created) 라는 튜플 형식으로 반환
        # 첫 번째 인자는 모델의 인스턴스, 두 번째 인자는 boolean flag
        # 두 번째 인자가 True 라면 인스턴스가 get_or_created 메서드에 의해 생성되었음, False 라면 인스턴스를 데이터베이스에서 꺼내왔음을 의미
        follow_info, created = FollowRelation.objects.get_or_create(
            follower=self,
            following=to_user,
            type=FollowRelation.UNAPPROVED,
        )

        if created:
            return follow_info
        else:
            return None

    def unfollow(self, from_user):
        """
        Delete follow_info object

        Args:
            from_user (An instance of UserFollowInfo):

        Returns:
            bool: True if successful, False otherwise.

        """
        # Follow Relation 을 삭제
        try:
            follow_info = FollowRelation.objects.get(
                follower=from_user,
                following=self,
                type=FollowRelation.APPROVED,
            )
            follow_info.delete()
            return True
        except follow_info.DoesNotExist:
            return False

    def approve(self, from_user):
        """
        Change the value 'UNAPPROVED' to 'APPROVED'

        Args:
            from_user (An instance of UserFollowInfo):

        Returns:
            bool: True if successful, False otherwise.

        """
        try:
            follow_info = FollowRelation.objects.get(
                follower=from_user,
                following=self,
                type=FollowRelation.UNAPPROVED,
            )
            follow_info.is_approved = FollowRelation.APPROVED
            follow_info.save()
            return True
        except follow_info.DoesNotExist:
            return False

    def reject(self, from_user):
        """
        Change the value 'UNAPPROVED' to 'REJECTED'

        Args:
            from_user (An instance of UserFollowInfo):

        Returns:
            bool: True if successful, False otherwise.

        """
        try:
            follow_info, created = FollowRelation.objects.get(
                follower=from_user,
                following=self,
                type=FollowRelation.UNAPPROVED,
            )
            follow_info.is_approved = FollowRelation.REJECTED
            follow_info.save()
            return True
        except follow_info.DoesNotExist:
            return False

    def get_following(self):
        """
        Returns the list of users that 'self' is following

        Returns:
            list: following

        """
        # 내가 follow 하고 있는 UserFollowInfo 목록 가져오기
        following_relation = self.followings.filter(type=FollowRelation.APPROVED)
        # values 는 해당 쿼리셋에서 각각을 키/값 딕셔너리로 바꾸어 반환
        # values_list 는 딕셔너리가 아닌 리스트 형태로 값들을 튜플로 만들어 리스트에 담아 반환
        following_list = following_relation.values_list('followings', flat=True)
        return FollowRelation.objects.filter(pk__in=following_list)

    def get_followers(self):
        """
        Returns the list of users following 'self'

        Returns:
            list: followers

        """
        # 나를 follow 하고 있는 UserFollowInfo 목록 가져오기
        follower_relation = self.followers.filter(type=FollowRelation.APPROVED)
        follower_list = follower_relation.values_list('followers', flat=True)
        return FollowRelation.objects.filter(pk__in=follower_list)

    class Meta:
        db_table = 'user_account'
        verbose_name = 'User Account'
        verbose_name_plural = f'{verbose_name} 목록'


class FollowRelation(TimestampedModel):
    # - 이 친구가 이제 FollowRelation 모델입니다.
    # - `UserA 가 UserB 를 팔로우하다` 대한 정의가 가능해야 합니다.
    # - User 모델은 `django.contrib.auth.models.User` 를 사용하시면 됩니다.
    # - 만들어지는 모델은 다음과 같은 표현이 가능해야합니다.
    #     - `UserA 는 UserB 를 팔로우하였으며, 아직 승인되지 않았다 / 승인되었다`
    CHOICES_TYPE = Choices(
        'APPROVED',
        'UNAPPROVED',
        'REJECTED'
    )

    # 같은 모델에 대해 ForeignKey 를 두 개 쓰고 있어서
    # 역참조 시에 어떤 모델을 참조해야 하는지 불분명해지므로 related_name 을 지정
    follower = models.ForeignKey(
        UserFollowInfo,
        on_delete=models.CASCADE,
        related_name='followers'
    )
    following = models.ForeignKey(
        UserFollowInfo,
        on_delete=models.CASCADE,
        related_name='followings'
    )

    # 승인됨/승인되지 않음을 표현하는 DB 상 필드
    is_approved = models.CharField(
        max_length=1,
        default='UNAPPROVED',
        choices=CHOICES_TYPE,
        related_name='is_approved'
    )

    def __str__(self):
        return f'{self.follower.user.username} -> {self.following.user.username}'

    class Meta:
        db_table = 'follow_relation'
        verbose_name = 'Follow Relation'
        verbose_name_plural = f'{verbose_name} 목록'
