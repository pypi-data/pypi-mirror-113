from onepasswd.onepasswd import *
from onepasswd import ltlog
import json

ltlog.getLogger("onepasswd.onepasswd").setLevel(ltlog.DEBUG)

log = ltlog.getLogger('onepasswd.test.gitdb')
log.setLevel(ltlog.INFO)
log.info('-----start test------')

git = GitDB('agfn', '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', 'onepasswd-db')


log.info("--------test github api---------")
ref = git._get_master()
log.debug(ref['object']['sha'])
com = git._get_commit(ref['object']['sha'])
tree = git._get_tree(com['tree']['sha'])
log.info('\n' + json.dumps(tree, indent=4))


db_info = git.get_db_info()

log.info('\n' + json.dumps(db_info, indent=4))

db = git.get_db(db_info)
log.info(db)


fp = open("onepasswd/test/db", "rb")
buf = fp.read()
resp = git._create_blob(buf)
log.info(json.dumps(resp, indent=4))
resp = git._create_tree({'sha': resp['sha']})
log.info('\n' + json.dumps(resp, indent=4))
resp = git._create_commit(resp['sha'], "test", [com['sha']])
log.info('\n' + json.dumps(resp, indent=4))
resp = git._update_master(resp['sha'])
log.info(resp)


log.info('*' * 20)
info = git.get_db_info()
log.info('db_info: ' + info['sha'] + ' parent: ' + info['commit'])
resp = git.push_db(b"{'12': 3}", info['commit'])
log.info(resp)
