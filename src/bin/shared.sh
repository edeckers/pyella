#!/usr/bin/env bash

function try_source_env () {
  if [ -f ${POETRY_HOME} ]; then
    export PATH="${POETRY_HOME}:${PATH}"
  fi
}

function poetry_path () {
  try_source_env

  echo `command -v poetry 2> /dev/null`
}

function assert_poetry_exists () {
  if [ -z `poetry_path` ]; then echo "Poetry could not be found. See https://python-poetry.org/docs/"; exit 2; fi
}

function p () {
  assert_poetry_exists
  `poetry_path` ${@}
}
