#!/usr/bin/env bash
git config "$@" user.name       tqfx
git config "$@" user.email      tqfx@foxmail.com
git config "$@" user.signingkey 54B434B4E27F1DCB
git config "$@" --unset         core.sshCommand
git config "$@" --list
