from onepasswd.crypto import *

ltlog.getLogger("onepasswd.crypto").setLevel(ltlog.DEBUG)


auth_info = generate_auth_info('ok')

auth(auth_info, 'ok')

