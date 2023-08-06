from rest_framework.response import Response
from dj_rest_auth.views import LoginView
from ..helpers import has_mfa


class MFALoginView(LoginView):
    """
    MFA Login View for session based MFA aware authentication
    If the user has MFA enabled, mark the session but don't log in
    Otherwise, use default behavior

    On a successful login with MFA enabled, return {"requires_mfa": true} with status code 200
    """

    def process_login(self):
        if has_mfa(self.request, self.user):
            self.user.mfa = True
        else:
            self.user.mfa = False
            super().process_login()

    def get_response(self):
        if self.user.mfa:
            return Response({"requires_mfa": True})
        return super().get_response()
