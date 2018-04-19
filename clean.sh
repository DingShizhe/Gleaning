#!/usr/bin/env bash

shopt -s extglob                # for bash
# setopt EXTENDED_GLOB          # for zsh

rm !(*.py|*.sh|*.tex|src|Makefile|*.pdf|README.md|*git*) -rf
