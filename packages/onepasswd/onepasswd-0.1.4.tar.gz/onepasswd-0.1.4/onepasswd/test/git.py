from onepasswd.onepasswd import GitDB
from onepasswd.config import Config
from onepasswd import ltlog

log = ltlog.getLogger('onepasswd.test.git')
log.setLevel(ltlog.DEBUG)

ltlog.getLogger('onepasswd.onepasswd').setLevel(ltlog.DEBUG)

conf = Config()

git = GitDB(conf['user'], conf['token'], conf['repo'])


root = git.get_root_dir_info()
log.debug(root)

file_info = git.get_file_info(root, 'db')
log.debug(file_info)

db = git.pull(file_info)
log.debug(db)

git.push('db', b'{}', root)
