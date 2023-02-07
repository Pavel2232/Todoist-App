from rest_framework import serializers

from core.serializers import UserSerializer
from goals.models import GoalCategory, Goal, GoalComment


class GoalCreateSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())


    class Meta:
        model = GoalCategory
        read_only_fields = ('id','created','update','user')
        fields = '__all__'




class GoalCategorySerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

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