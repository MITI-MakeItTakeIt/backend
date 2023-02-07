from django.core.mail import EmailMessage


class UserActivationEmail(EmailMessage):
    
    def __init__(self, uidb64=None, token=None, to=None):
        super().__init__(
            subject = "[MITI]회원가입 인증 메일",
            body = f"미티에 가입하신 것을 환영합니다!\n미티의 다양한 서비스를 사용하고 싶으시다면 아래의 링크를 클릭해주세요.\nhttp://127.0.0.1:8000/users/activate/{uidb64}/{token}/",
            to=to
            )
