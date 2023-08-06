from os import name
from os.path import join
import sys


log_file = ''
PASSWORD_DB = ''
USER_DB = ''
login_ui = ''
create_acc_ui = ''
pass_table_ui = ''
save_info_ui = ''

paths = sys.path
for path in paths:
    if 'site-packages' in path:
        log_file = join(path,'safepass','logs','SafePass.log')
        PASSWORD_DB = join(path,'safepass','db','passwords.db')
        USER_DB = join(path,'safepass','db','users.db')
        login_ui = join(path,'safepass','ui','login.ui')
        create_acc_ui = join(path,'safepass','ui','CreateAccount.ui')
        pass_table_ui = join(path,'safepass','ui','PasswordsTable.ui')
        save_info_ui = join(path,'safepass','ui','SaveInfo.ui')
