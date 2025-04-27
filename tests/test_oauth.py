from connectai.lark.websocket import *


class OAuthBot(Bot):
    def on_message(self, data, *args, **kwargs):
        if 'code' in data:
            access = self.post(
                f"{self.host}/open-apis/authen/v1/oidc/access_token",
                json=dict(
                    grant_type="authorization_code",
                    code=data['code'],
                ),
                headers={
                    "Authorization": f"Bearer {self.app_access_token}",
                },
            ).json()
            print("access", access)
            user_info = self.get(
                f"{self.host}/open-apis/authen/v1/user_info",
                headers={
                    "Authorization": f"Bearer {access['data']['access_token']}",
                },
            ).json()
            print("user_info", user_info)


bot = OAuthBot(
    app_id="",
    app_secret="",
)
client = Client(bot, server="feishu.fieldshortcut.com", protocol="http")
client.start(debug=True)
