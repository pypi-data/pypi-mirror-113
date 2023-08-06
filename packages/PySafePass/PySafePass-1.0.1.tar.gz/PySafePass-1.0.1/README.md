# SafePass

```
=================================================
      __        __        ___              
     / _\ __ _ / _| ___  / _ \__ _ ___ ___ 
     \ \ / _` | |_ / _ \/ /_)/ _` / __/ __|
     _\ \ (_| |  _|  __/ ___/ (_| \__ \__ \
     \__/\__,_|_|  \___\/    \__,_|___/___/
     ~ ~ An Open Source Password Manager ~ ~
================================================= 
```

SafePass is an Open Source Password Manager which stores usernames, passwords and websites with multiple user option. User can create multiple users and store their information securely from other SafePass users. Users can save and fetch passwords along with other operations using SafePass Terminal. SafePass also provides user to generate random passwords.

## About SafePass

SafePass was previously written in JAVA as random password generator, SafePass is now ported to python3 providing new features like multiple users funnctionality, options to generate, save and fetch passwords from the user stored database. 


## Dependencies
`SafePass` requires following programs/libraries/modules to run properly:
  - `Python`
    - `prettytable`
    - `cryptography`

## Installation

### For Windows

- Install [Python3](https://www.python.org/) and [git](https://git-scm.com/) on your Windows.

- Check if python and git are installed and added to the path. Open Powershell or Command Prompt.
  - Python
  ```
  PS C:\Users\User> python --version
  Python 3.9.5
  ```
  - git 
  ```
  PS C:\Users\User> git --version
  git version 2.30.1.windows.1
  ```
  > Note: If your output is not similar to above, try adding python and git to environment variables path.

- Clone the SafePass repository 
  ```
  PS C:\Users\User> git clone https://github.com/dmdhrumilmistry/safepass
  ```
  
- Change directory to safepass
  ```
  PS C:\Users\User> cd safepass
  ```
  
- Install requirements
  ```
  PS C:\Users\User\safepass> pip install -r requirements.txt
  ```
  
- Run the safepass python file to start SafePass
  ```
  PS C:\Users\User\safepass> python safepass.py
  ```


### For Debian based distros

- Install python3 and git
  ```
  $ sudo apt update -y && sudo apt upgrade -y && sudo apt install python3 python3-pip git build-essential libssl libffi rust -y
  ```
  
- Check if python3 and git are installed properly
  ```
  $ python --version && git --version
  Python 3.9.5
  git version 2.20.1
  ```
  
- Clone the SafePass repository
  ```
  $ git clone https://github.com/dmdhrumilmistry/safepass
  ```

- Change directory to safepass
  ```
  $ cd safepass
  ```
  
- Install requirements
  ```
  $ pip3 install -r requirements.txt
  ```
 
- Run SafePass
  ```
  $ python3 safepass.py
  ```
 
 
 ### On Android (Using Termux)
 
- Install python3 and git
  ```
   $ pkg update -y && pkg upgrade -y && pkg install python git build-essential libffi rust -y
  ```
  
- Check if python3 and git are installed properly
  ```
  $ python --version && git --version
  Python 3.9.5
  git version 2.32.0
  ```
  
- Clone the SafePass repository
  ```
  $ git clone https://github.com/dmdhrumilmistry/safepass
  ```

- Change directory to safepass
  ```
  $ cd safepass
  ```
  
- Install requirements
  ```
  $ pip3 install -r requirements.txt
  ```
 
- Run SafePass
  ```
  $ python3 safepass.py
  ```
 
 
 ## SafePass Terminal Commands 
 
 | Commands | Usage |
 |:--------:|:-----|
 | login |authenticate user to login into their accounts |
 |newuser|create a new user|
 |savepass|encrypts and saves user information to the database|
 |getpass|retrieves user information from the database and decrypts it|
 |show|prints user information (usernames, websites and passwords)|
 |help|prints help menu|
 |clear|clears text on the screen|
 |exit|exit safepass|
 
## Have Any Issues or Idea 💡

- Create an issue
- Fork this repo, add new feature and create Pull Request. 


## Star⭐ SafePass repository
