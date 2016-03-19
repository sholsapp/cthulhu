#!/bin/bash

# GENERATED CONTROL SCRIPT

sub_help() {
  echo "Usage: control <subcommand> [options]"
  echo "Subcommands:"
  echo "    start"
  echo "    stop"
}

sub_start() {
{% for instance in instances %}
  {{ instance.node_control }} start
{% endfor %}
}

sub_stop() {
  RUNNING_CONTAINERS=$(docker ps -q)
  if [ "$RUNNING_CONTAINERS" != "" ]; then
    OUT="$(docker stop -t 1 $RUNNING_CONTAINERS)"
  fi

  OLD_CONTAINERS="$(docker ps -a -q)"
  if [ "$OLD_CONTAINERS" != "" ]; then
    OUT="$(docker rm $OLD_CONTAINERS)"
  fi
}

SUBCOMMAND=$1
case $SUBCOMMAND in
  "" | "-h" | "--help")
    sub_help
    ;;
  *)
    shift
    sub_${SUBCOMMAND} $@
    if [ $? = 127 ]; then
      echo "Error: '$SUBCOMMAND' is not a known subcommand." >&2
      exit 1
    fi
    ;;
esac
