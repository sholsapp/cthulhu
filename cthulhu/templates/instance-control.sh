#!/bin/bash -x

# GENERATED CONTROL SCRIPT

sub_help() {
  echo "Usage: control <subcommand> [options]"
  echo "Subcommands:"
  echo "    start"
  echo "    stop"
}

sub_start() {
  PID=$(docker run \
    --privileged=true \
    --name {{ name }} \
    --interactive \
    --tty \
    --detach \
    --publish={{ host_port }}:8080 \
    --hostname={{ host_name }} \
    --volume={{ local_etc }}:/opt/app/etc \
    --volume={{ local_var }}:/opt/app/var \
    --memory=16M \
    {{ docker_image }})
  echo $PID > {{ local_root }}/pid.txt
}

sub_stop() {
  docker stop -t 1 {{ name }}
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
