import json
import os

from jinja2 import Environment, PackageLoader


class InstanceContext(object):
    """An instance context.

    An instance context is a part larger fixture and captures context specific
    to this instance, e.g., the instance's file system root, configuration
    directory, log file, and more.

    """

    def __init__(self, root, instance, network, container):
        self.instance = instance
        self.network = list(network)
        self.container = container
        self.node_root = os.path.join(root, str(self.network[self.instance]))
        self.node_bindmounts = os.path.join(self.node_root, 'bindmounts')
        self.node_etc = os.path.join(self.node_bindmounts, 'etc')
        self.node_var = os.path.join(self.node_bindmounts, 'var')

        os.makedirs(self.node_root)
        os.makedirs(self.node_bindmounts)
        os.makedirs(self.node_etc)
        os.makedirs(self.node_var)

        self.node_config = os.path.join(self.node_etc, 'config.json')
        self.node_control = os.path.join(self.node_root, 'control')
        self.node_log = os.path.join(
            self.node_var, '{0}.log'.format(self.instance_name))

    def write_file(self, path, contents, perm=0o644):
        with open(path, 'w') as fh:
            fh.write(contents)
        os.chmod(path, perm)

    def formatted_instance(self):
        return 'i{0}'.format(str(self.instance + 1).zfill(3))

    @property
    def instance_name(self):
        return self.formatted_instance()

    def render(self):
        self.write_file(self.node_config,
                        self.render_config())
        self.write_file(self.node_control,
                        self.render_control(),
                        perm=0o755)
        self.write_file(self.node_log, '')

    def render_config(self):
        # TODO(sholsapp): How can we make this generic but meaningful? We always will
        # need to know a little bit about the application here, so maybe we should
        # ask for a fixture.spec or something?
        ip = self.network[self.instance]
        return json.dumps({
            'self': str(ip),
            'port': 8080,
            'master': True if ip == self.network[0] else False,
            'peers': [str(n) for n in self.network if n != ip],
        }, indent=2)

    def render_control(self):
        host_port = 30000 + self.instance
        host_name = self.instance_name
        env = Environment(loader=PackageLoader('cthulhu', 'templates'))
        template = env.get_template('instance-control.sh')
        # TODO(sholsapp): How can we make this generic but meaningful? We always will
        # need to know a little bit about the application here, so maybe we should
        # ask for a fixture.spec or something?
        return template.render(
            docker_container=self.container,
            host_name=host_name,
            host_port=host_port,
            local_etc=self.node_etc,
            local_root=self.node_root,
            local_var=self.node_var,
            name=self.instance_name,
        )
