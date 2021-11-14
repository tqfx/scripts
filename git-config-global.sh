#!/usr/bin/env bash
# Set default branch when init
git config --global init.defaultbranch master
# Set gpg sign when commit
git config --global commit.gpgsign true
# Set gpg sign when tag
git config --global tag.forcesignannotated true
# Convert crlf to lf
git config --global core.autocrlf input
# Ignore file mode
git config --global core.filemode false
# Don't ignore case
git config --global core.ignorecase false
# Cancel quote path
git config --global core.quotepath false
# Enable long path
git config --global core.longpaths true
# Set date format
git config --global log.date format:'%Y-%m-%d %H:%M:%S'
git config --global blame.date format:'%Y-%m-%d %H:%M:%S'
git config --global reflog.date format:'%Y-%m-%d %H:%M:%S'
# Set encoding to utf-8
git config --global i18n.commitEncoding utf-8
git config --global i18n.logOutputEncoding utf-8
# Set ui color auto
git config --global color.ui auto
# Store credential
git config --global credential.helper store
# Set submodule recurse
git config --global submodule.recurse true
# Set lfs prune verify remote always
git config --global lfs.pruneverifyremotealways true
# Set gui encoding
git config --global gui.encoding utf-8
# List global config
git config --global --list
