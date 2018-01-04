#!/usr/bin/env python

"""Create a distributed test fixture for use on a Unix-like system.

This tool creates a file system on disk that can be used to start n-many docker
containers. Each docker container started using the control script will
automatically have a configuration and log bind mount created and linked to the
respective container.

It is said that this tool creates a distributed test *fixture* because no
assertions are codified or made by this tool or its generated files. Instead,
only set up and tear down states are provided by this tool. All assertions
should be codified and made by an external driver like bats.

"""

import click
import json
import logging
import os
import sys

from netaddr import IPAddress, IPRange
from jinja2 import Template
import netifaces

from cthulhu.fixture import FixtureContext
from cthulhu.instance import InstanceContext


logging.basicConfig(level=logging.INFO)
log = logging.getLogger(__name__)


@click.command(help=__doc__, epilog='Currently, only usable within the context of gallocy.')
@click.option('--instances', default=1,
              help='The number of instances to create skeletons for.')
@click.option('--docker-bridge', default='docker0',
              help='The docker bridge network within which to create the distributed test fixture.')
@click.option('--docker-image', default='app',
              help='The docker image to wire into the distributed test fixture.')
@click.option('--fixture-root', default=os.getcwd(),
              help='Path to file system root directory at which to create the fixture.')
@click.option('--fixture-name', default='cthulhu-fixture',
              help='Name of the fixture and directory to create.')
def main(instances, docker_bridge, docker_image, fixture_root, fixture_name):

    try:
        addrs = netifaces.ifaddresses(docker_bridge)
    except ValueError:
        click.secho('It appears {0} is not a valid newtork interface on this system.'.format(
            docker_bridge), fg='red')
        sys.exit(1)

    try:
        docker_bridge_addr = IPAddress(addrs[netifaces.AF_INET][0]['addr'])
    except IndexError:
        click.secho('It appears {0} does not have an address at this time.'.format(docker_bridge), fg='red')
        sys.exit(1)

    network = list(IPRange(docker_bridge_addr + 1,
                           docker_bridge_addr + 1 + instances - 1))

    if os.path.exists(os.path.join(fixture_root, fixture_name)):
        click.secho('[ERROR] ', fg='red', nl=False)
        click.secho('A fixture named {0} already exists.'.format(fixture_name))
        sys.exit(1)

    fixture_ctx = FixtureContext(fixture_root, fixture_name)

    for instance in range(0, len(network)):
        # TODO(sholsapp): We might want to specify different containers for
        # different instances one day.
        instance_ctx = InstanceContext(
            fixture_ctx.fixture_root, instance, network, docker_image)
        click.secho('Creating instance {0} at {1}... '.format(
            instance_ctx.instance, instance_ctx.node_root), nl=False)
        fixture_ctx.instances.append(instance_ctx)
        click.secho('[GOOD]', fg='green')
    fixture_ctx.render()
