import json
import os

from jinja2 import Environment, PackageLoader


class FixtureContext(object):
    """A fixture context.

    A fixture context is a distributed control framework codified onto the file
    system and runnable through docker.

    :param str root: The root directory in which to create the fixture.
    :param str name: The name of the fixture.

    """

    def __init__(self, root, name):
        self.instances = []
        self.fixture_root = os.path.join(root, name)
        self.fixture_control = os.path.join(self.fixture_root, 'control')
        self.fixture_spec = os.path.join(self.fixture_root, 'spec.json')
        os.makedirs(self.fixture_root)

    def write_file(self, path, contents, perm=0o644):
        with open(path, 'w') as fh:
            fh.write(contents)
        os.chmod(path, perm)

    def render(self):
        # Render all instances
        for instance in self.instances:
            instance.render()
        # Render human readable links to each instance
        for instance in self.instances:
            try:
                os.symlink(instance.node_root, os.path.join(
                    self.fixture_root, instance.instance_name))
            except Exception:
                log.exception('Failed to create symlink to %s',
                              instance.instance_name)
        # Render the master control script
        self.write_file(self.fixture_control,
                        self.render_control(), perm=0o755)

        # Render the fixture specification file
        self.write_file(self.fixture_spec,
                        self.render_spec())


    def render_control(self):
        env = Environment(loader=PackageLoader('cthulhu', 'templates'))
        template = env.get_template('fixture-control.sh')
        return template.render(
            instances=self.instances,
        )

    def render_spec(self):
        spec = {}
        for instance in self.instances:
            spec[instance.instance_name] = {
                'root': instance.node_root,
                'port': instance.exposed,
                'ip': instance.ip,
            }
        return json.dumps(spec, indent=4)
