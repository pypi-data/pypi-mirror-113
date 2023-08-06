from setuptools import setup, find_packages

setup(
    name = 'PySafePass',
    version = '1.0.1',
    license='MIT License',
    description = 'SafePass is an Open Source Password Manager.',
    long_description = 'SafePass is an Open Source Password Manager which stores usernames, passwords and websites with multiple user option. User can create multiple users and store their information securely from other SafePass users. Users can save and fetch passwords along with other operations using SafePass Terminal. SafePass also provides user to generate random passwords.',
    packages=find_packages(),
    package_data = {'UI':['CreateAccount.ui','login.ui','PasswordsTable.ui','SaveInfo.ui']},
    include_package_data = True,
    install_requires = ['pyqt5',
                         'pyperclip', 
                         'cryptography',
                          'pyqt5-tools'],

)