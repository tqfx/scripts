#!/usr/bin/env bash
FLAGS+=" --no-line-number"
FLAGS+=" --no-round-corner"
FLAGS+=" --no-window-controls"
FLAGS+=" --font Consolas"
FLAGS+=" --line-offset 0"
FLAGS+=" --line-pad 0"
FLAGS+=" --pad-horiz 0"
FLAGS+=" --pad-vert 0"
silicon $FLAGS $@
