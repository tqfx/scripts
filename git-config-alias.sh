#!/usr/bin/env bash
git config --global alias.st "status -sb"
git config --global alias.undo "reset --soft HEAD^"
git config --global alias.amend "commit --amend --no-edit"
git config --global alias.lg "log --graph --pretty=format:'%Cred%h%Creset -%C(yellow)%d%Creset %s %Cgreen(%cr) %C(bold blue)<%an>%Creset'"
git config --global alias.rank "shortlog -n -s --no-merges"
