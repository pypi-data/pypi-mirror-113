***************************************************************************
rmti - An AI application that determines your Myers-Briggs Type Indicator.
***************************************************************************

Description
#############
Right now the app only contains a bot that mines data from Reddit. In the future we are planning on using that 
data along with some machine learning algorithms to be able to predict people's types. 

Setup
#######

We are currently working on a setup.py script that will make setting this up really easy. For now just clone the project and follow the steps below.

1. If you do not already have a Reddit application or bot go to `Reddit <reddit.com/prefs/apps>`_ and create an app. One you do 
that you should be able to obtain your own ``client_id`` and ``client_secret``. Use ``http://localhost:8080`` as your redirect uri or your user context such as a web site.

2. To protect your credentials create a ``praw.ini`` file inside of your root directory. Then place your credentials inside of this file. This is not the best 
way to authenticate but it will do for now. We plan on moving toward a token based authentication later on. The password and username are the ones you use 
to sign into your reddit account. It should look like this - 

| [YourBot]
| client_id=...
| client_secret=...
| password=...
| username=..


3. Install all modules in requirements.txt using ``pip install -r requirements.txt``. If you still need to import modules then run 
``pip install <module>`` and make a note taht we need to add that module to the requirements.txt. ``requirements.txt`` will be replaced when we establish our setup.py. 

4. Configure and create a Reddit intances with ``praw.Reddit('YourBot')`` inside of ``redditbot.py``. 
Just modify this line of code: ``reddit = praw.Reddit('bot1', config_interpolation="basic")``. config_interpolation="basic" is not necessary unless you plan on adding more detail to your bot such as author and version. 

5. Now you should be able to run the redditbot in multiple ways. Either using it as a module somewhere in the project, 
running it as a script on the command line or even importing it into a Jupyter Notebook file. 

Resources 
###############

`PRAW Docs <https://praw.readthedocs.io/en/v7.3.0/>`_
