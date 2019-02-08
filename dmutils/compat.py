from itsdangerous import URLSafeTimedSerializer
from flask.sessions import SecureCookieSessionInterface


class DMURLSafeTimedSerializer(URLSafeTimedSerializer):
    def sign(self):
        """Do our own encode"""


    def unsign(self, session_cookie):
        """Do our own decode"""




class DMSecureCookieSessionInterface(SecureCookieSessionInterface):

    def get_signing_serializer(self, app):
        if not app.secret_key:
            return None
        signer_kwargs = dict(
            key_derivation=self.key_derivation,
            digest_method=self.digest_method
        )
        return DMURLSafeTimedSerializer(app.secret_key, salt=self.salt,
                                        serializer=self.serializer,
                                        signer_kwargs=signer_kwargs)


class DMFlask(Flask):
    session_interface = DMSecureCookieSessionInterface

MutliDecodeCompatibilityApp = DMFlask

