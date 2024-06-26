# 2024-IST-T1

## Brief

This project is created as a standalone python game that runs in the terminal, as an answer to the text-based criteria of **Assessment No.1** of this year

Do note that this game will only function correctly on OSX devices.
If the native mac terminal is a bit buggy then just quit and refresh it
Expansion releases (if I bother with them) will be released on here.
Honestly for me the best way to run and keep up to date is just to `gh repo clone Icecreambobcat/2024-IST-T1` the repo and `git pull` in the repo whenever you want to update.

- Do note that a requisite of this is downloading the official Github CLI tool which can be done easily via `brew install gh` on homebrew.
- Since some stuff is blocked just run `git clone https://github.com/Icecreambobcat/2024-IST-T1.git` once you have git

Do be sure though to maintain a copy of `save.dat` to keep your progress.

[Here's](https://www.icloud.com/freeform/02cHPE95WhLR1DRTar9rz-5xw) a link to see the approximate story layout for the game and any upcoming expansions. This story and any other characters present are my intellectual property, and reuse without written permission is prohibited.

## How do I run the game?

Don't worry, I planned around this being a bit of a pain to mark and release, so I included dedicated scripts and programs to help run the code.

However, due to the fact that this game was designed around the native OSX terminal, it'll function best when launched into it via the scripts rather than the compatability version launched from vscode. Thus, you'll need access to your native terminal to run this.

### You still didn't tell me how to run it

Wait, ok, I'm getting round to it.

First, some requisites:

- Python 3.12 and the modules:
  - Pickle
  - Curses
  - Random
  - csv
  - Time
  - OS

If you don't have any or some of these, I recommend downloading [homebrew](brew.sh) for a fresh install of python as well as downloading [pygame](https://www.pygame.org/wiki/GettingStarted) should you not have the `pip` or `pip3` tools.
This can be checked by running `pip3 --version` or `pip --version` in your terminal

### And you're going to tell me that you don't have access to the terminal

It's a simple fix really, you just have to be able to run as root, but don't blame me for what happens next should you accidentally `rm -rf` your root directory.

You can choose between [vscode](https://code.visualstudio.com/) or [iterm2](https://iterm2.com/) for your terminal options, and frankly, it doesn't matter that much for most of you anyways. What you're going to do is launch into the terminal and type the following:
```sudo visudo```
What this'll do is take you to your sudoers file after entering your password, launching a vim edit session which is the only way you can edit this file.
Then, add `<YOUR_USERNAME> ALL = (ALL) ALL` to the bottom where you see `%admin ALL = (ALL) ALL`
If you don't know your username, run `whoami` in the shell

If it still doesn't work run `sudo jamf removeFramework`

After that, you're basically done

## So, what next?

After that, open up your native terminal and enter the following:

```zsh
chmod +x ~/<YOUR_USERNAME>/path_to_file/runscript.zsh
cd ~/<YOUR_USERNAME>/path_to_file
./.runscript.zsh launcher.py
```

You should be good to go from there!

Alternatively, just run the launcher file from vscode, and if you have access to your terminal it should work.

### Misc

To reset:

```zsh
cd ~/<YOUR_USERNAME>/path_to_file
./.runscript.zsh reset.py
```

Alterntive run method is the same as launch

MAN this project was a pain
but yeah if you cbf just run it in vscode it'll suck a bit but oh well
