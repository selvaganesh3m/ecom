import graphene
from customers.schema import UserType
from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from django.conf import settings
from customers.models import User
from django.core.cache import cache
import math
import random
from graphql_jwt.shortcuts import get_token, get_user_by_token


class UserSignUp(graphene.Mutation):
    class Arguments:
        email = graphene.String()
        password = graphene.String()

    user = graphene.Field(UserType)

    def mutate(self, info, email, password):
        user = get_user_model().objects.create_user(email=email, password=password)
        return UserSignUp(user=user)


class UserLoginEmail(graphene.Mutation):
    message = graphene.String()

    class Arguments:
        email = graphene.String(required=True)

    def mutate(self, info, email):

        # OTP generation
        digits = [i for i in range(0, 10)]
        otp = ''

        for i in range(6):
            index = math.floor(random.random() * 10)
            otp += str(digits[index])
        # end for

        try:
            user = User.objects.get(email=email)
            response = send_mail(
                'Graphene-Django Login',
                f'Please use OTP:  {otp} to Login.',
                settings.EMAIL_HOST_USER,
                [user.email],
                fail_silently=False,
            )
            if response:
                cache.set(user.email, otp, 300)
                return UserLoginEmail(message="OTP has been sent to your mail.")
                # endif
            return UserLoginEmail(message="Unable to send OTP, Please try after sometime.")
        except User.DoesNotExist:
            return UserLoginEmail(message="Please SignUp.")


class UserOTP(graphene.Mutation):
    message = graphene.String()
    token = graphene.String(required=True)

    class Arguments:
        email = graphene.String(required=True)
        otp = graphene.String(required=True)

    def mutate(self, info, otp, email):
        cache_otp = cache.get(email)
        if not cache_otp:
            return UserOTP(message="OTP Expired. Please request Again.")
        if otp != cache_otp:
            return UserOTP(message="Invalid OTP.")
        user = User.objects.get(email=email)
        return UserOTP(message=f"Welcome, LoggedIn Successfully.", token=get_token(user))


class UserLogOut(graphene.Mutation):
    message = graphene.String()

    def mutate(self, info):
        print(info.context.user)
        return UserLogOut(message="Logged Out Successfully.")


class UserMutation(graphene.ObjectType):
    user_signup = UserSignUp.Field()
    user_login_email = UserLoginEmail.Field()
    user_login_otp = UserOTP.Field()
    user_logout = UserLogOut.Field()
