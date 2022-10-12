from authentication.models import User


def get_user(*, user: User):
    return {
        'id': user.id,
        'username': user.name,
        'email': user.email
    }


def jwt_response_payload_handler(token, user=None, request=None):
    return {
        'token': token,
        'user': get_user(user=user),
    }


 # token = RefreshToken.for_user(user).access_token
        # current_site = get_current_site(request).domain #get the site the app is on currently
        # relative_url = reverse('verify-email')
        # absolute_url  = "http://" + current_site + relative_url + "?token=" + str(token)
        # body = f"Hi {user.username}, verify your email with  this link \n {absolute_url}"
        # subject = 'email verification'
        # from_mail = 'devgentlesoul18@gmail.com'

        # data = {'email_subject':subject, 'email_body':body, 'from_email':from_mail, 'to_email':[user.email]}

        # send_mail(data)


    # class VerifyEmailView(GenericAPIView):
    # swagger_schema = None
    # def get(self, request):
    #     token =request.GET.get('token')



    #     try:
    #         payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
    #         user = User.objects.get(id=payload['user_id'])

    #         if not user.is_verified:
    #             user.is_verified = True
    #             user.save()
    #         return Response(redirect(f'{settings.BASE_FRONTEND_URL}')) #redirects user to home page
    #     # if token has expired
    #     except jwt.ExpiredSignatureError as identifier:
    #         return Response(
    #             {'timeout':'token has expired'}
    #         )
    #     #if token has been tampered with
    #     except jwt.exceptions.DecodeError as identifier:
    #         return Response(
    #             {'error':'invalid token'}
    #         )