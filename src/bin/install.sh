#!/usr/bin/env bash

function cd_to_source_directory () {
  cd `dirname ${0}`/..
}

function install_git_hooks () {
  p run pre-commit install
  p run pre-commit install --hook-type commit-msg
}

function install_poetry () {
  if [ -z ${POETRY} ]; then
    # FIXME ED The poetry installer is pinned to version 1.8.5, because the 2.0.0
    #          release breaks the build. We need to support 2.0.0 in the future though.
    curl -sSL https://install.python-poetry.org/ |  POETRY_VERSION=1.8.5 python -

    try_source_env
  fi
}

function install () {
  p install
}

cd_to_source_directory

source bin/shared.sh

install_poetry
install
install_git_hooks
