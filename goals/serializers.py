from django.db import transaction
from rest_framework import serializers

from core.models import User
from core.serializers import UserSerializer
from goals.models import GoalCategory, Goal, GoalComment, BoardParticipant, Board


class GoalCreateSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    board = serializers.SlugRelatedField(
        queryset=Board.objects.all(),
        required=True,
        slug_field='id'
    )

    class Meta:
        model = GoalCategory
        read_only_fields = ('id','created','update','user')
        fields = '__all__'




class GoalCategorySerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    board = serializers.SlugRelatedField(
        required=False,
        read_only=True,
        slug_field='id'
    )
    class Meta:
        model = GoalCategory
        fields = "__all__"
        read_only_fields = ("id", "created", "updated", "user")


class GoalGoalCreateSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    category = serializers.SlugRelatedField(
        required=False,
        queryset=GoalCategory.objects.all(),
        slug_field = "id"
    )
    class Meta:
        model = Goal
        fields = "__all__"
        read_only_fields = ("id", "created","update")


    def validate_category(self, value):
        if value.is_deleted:
            raise serializers.ValidationError("not allowed in deleted category")

        if value.user != self.context["request"].user:
            raise serializers.ValidationError("not owner of category")

        return value




class GoalSerializer(serializers.ModelSerializer):
    category = GoalCategorySerializer(read_only=True)
    user = UserSerializer(read_only=True)

    class Meta:
        model = Goal
        fields = "__all__"
        read_only_fields = ("id", "created", "updated", "user",)



class CommentCreateSerializer(serializers.ModelSerializer):
    """Создание комментария"""
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    goal = serializers.SlugRelatedField(
        required=False,
        queryset=Goal.objects.all(),
        slug_field= "id"
    )

    class Meta:
        model = GoalComment
        fields = "__all__"
        read_only_fields = ("id", "created","update")


    def validate_comment(self, value):
        if value.is_deleted:
            raise serializers.ValidationError("not allowed in deleted goal")

        if value.user != self.context["request"].user:
            raise serializers.ValidationError("not owner of goal")

        return value


class CommentSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    goal = GoalSerializer(read_only=True)

    class Meta:
        model = GoalComment
        fields = "__all__"
        read_only_fields = ("id", "created", "updated", "user")

class BoardCreateSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Board
        read_only_fields = ("id", "created", "updated")
        fields = "__all__"

    def create(self, validated_data):
        user = validated_data.pop("user")
        board = Board.objects.create(**validated_data)
        BoardParticipant.objects.create(
            user=user, board=board, role=BoardParticipant.Role.owner
        )
        return board


class BoardParticipantSerializer(serializers.ModelSerializer):
    role = serializers.ChoiceField(
        required=True, choices=BoardParticipant.Role
    )
    user = serializers.SlugRelatedField(
        slug_field="username", queryset=User.objects.all()
    )

    class Meta:
        model = BoardParticipant
        fields = "__all__"
        read_only_fields = ("id", "created", "updated", "board")


class BoardSerializer(serializers.ModelSerializer):
    participants = BoardParticipantSerializer(many=True)
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Board
        fields = "__all__"
        read_only_fields = ("id", "created", "updated")

    def update(self, instance, validated_data):
        owner = validated_data.pop("user")
        new_participants = validated_data.pop("participants")
        new_by_id = {part["user"].id: part for part in new_participants}

        old_participants = instance.participants.exclude(user=owner)
        with transaction.atomic():
            for old_participant in old_participants:
                if old_participant.user_id not in new_by_id:
                    old_participant.delete()
                else:
                    if (
                            old_participant.role
                            != new_by_id[old_participant.user_id]["role"]
                    ):
                        old_participant.role = new_by_id[old_participant.user_id][
                            "role"
                        ]
                        old_participant.save()
                    new_by_id.pop(old_participant.user_id)
            for new_part in new_by_id.values():
                BoardParticipant.objects.create(
                    board=instance, user=new_part["user"], role=new_part["role"]
                )

            instance.title = validated_data["title"]
            instance.save()

        return instance

class BoardListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Board
        fields = "__all__"