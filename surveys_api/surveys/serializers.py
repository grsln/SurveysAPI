from rest_framework import serializers

from .models import Answer, Question, SimpleSurvey, SimpleSurveyResult, User


class TokenObtainPairResponseSerializer(serializers.Serializer):
    access = serializers.CharField()
    refresh = serializers.CharField()

    def create(self, validated_data):
        raise NotImplementedError()

    def update(self, instance, validated_data):
        raise NotImplementedError()


class TokenRefreshResponseSerializer(serializers.Serializer):
    access = serializers.CharField()

    def create(self, validated_data):
        raise NotImplementedError()

    def update(self, instance, validated_data):
        raise NotImplementedError()


class AnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Answer
        fields = ("id", "answer")


class ResultSerializer(serializers.ModelSerializer):
    class Meta:
        model = SimpleSurveyResult
        fields = ("id", "answered_id", "question")

    def update(self, instance, validated_data):
        instance.answered_id = validated_data.get("answered_id", instance.answered_id)
        instance.save()
        return instance


class QuestionSerializer(serializers.ModelSerializer):
    answers = AnswerSerializer(many=True, read_only=True)

    class Meta:
        model = Question
        fields = ("id", "question", "answers")


class QuestionResSerializer(serializers.ModelSerializer):
    answers = AnswerSerializer(many=True, read_only=True)

    class Meta:
        model = Question
        fields = ("id", "question", "answers", "right_answer")


class SimpleSurveySerializer(serializers.ModelSerializer):
    questions = QuestionSerializer(many=True, read_only=True)
    simple_surveys_result = ResultSerializer(
        source="simple_surveys_result_set", many=True
    )

    class Meta:
        model = SimpleSurvey
        fields = (
            "id",
            "simple_survey_date",
            "status",
            "questions",
            "simple_surveys_result",
        )
        read_only_fields = ["id", "simple_survey_date", "status", "questions"]


class SimpleSurveyResSerializer(serializers.ModelSerializer):
    questions = QuestionResSerializer(many=True, read_only=True)
    simple_survey_result = ResultSerializer(
        source="simple_survey_result_set", many=True
    )

    class Meta:
        model = SimpleSurvey
        fields = (
            "id",
            "simple_survey_date",
            "status",
            "questions",
            "simple_survey_result",
        )
        read_only_fields = ["id", "simple_survey_date", "status", "questions"]


class CustomUserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=True)
    username = serializers.CharField()
    password = serializers.CharField(min_length=8, write_only=True)

    def validate_email(self, value):
        ModelClass = self.Meta.model
        if ModelClass.objects.filter(email=value).exists():
            raise serializers.ValidationError("already exists")
        return value

    class Meta:
        model = User
        fields = ("email", "username", "password")
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
        password = validated_data.pop("password", None)
        instance = self.Meta.model(**validated_data)
        if password is not None:
            instance.set_password(password)
        instance.save()
        return instance


class CustomUserEditSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=True)
    username = serializers.CharField()
    password = serializers.CharField(min_length=8, write_only=True)

    class Meta:
        model = User
        fields = ("email", "username", "password")
        extra_kwargs = {"password": {"write_only": True}}

    def update(self, instance, validated_data):
        instance.username = validated_data.get("username", instance.username)
        instance.password = validated_data.get("password", instance.password)
        instance.save()
        return instance
