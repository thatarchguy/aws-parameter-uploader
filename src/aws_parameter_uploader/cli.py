"""
Module that contains the command line app.

Why does this file exist, and why not put this in __main__?

  You might be tempted to import things from __main__ later,but that will cause
  problems: the code will get executed twice:

  - When you run `python -m aws_parameter_uploader` python will execute
    ``__main__.py`` as a script. That means there won't be any
    ``aws_parameter_uploader.__main__`` in ``sys.modules``.
  - When you import __main__ it will get executed again (as a module) because
    there's no ``aws_parameter_uploader.__main__`` in ``sys.modules``.

  Also see (1) from http://click.pocoo.org/5/setuptools/#setuptools-integration
"""
import boto3
import click
try:
    from configparser import ConfigParser
except ImportError:
    from ConfigParser import ConfigParser


class SMPSUploader(object):
    """
    Class for the aws-parameter-uploader
    """

    def __init__(self, namespace, env):
        """
        Initialize the SMPSUploader class

        Args:
            None

        Returns:
            The boto3 SSM class object
        """
        self.client = boto3.client('ssm')
        self.namespace = namespace
        self.env = env

    def set(self, container, parameter, value):
        """Set a parameter's value

        Args:
            container: config section header (like the header section in an ini file)
            parameter: Boolean parameter to get
            value: String to set parameter
        Returns:
            Boolean
        """
        response = self.client.put_parameter(Name="{0}.{1}.{2}.{3}".format(self.namespace,
                                                                           self.env,
                                                                           container,
                                                                           parameter),
                                             Value=value,
                                             Type='String',
                                             Overwrite=True)
        return True if response.get('ResponseMetadata', {}).get('HTTPStatusCode') == 200 else False

    def upload(self, filename):
        """
        Parse a config ini file into AWS Systems Manager Parameter Store

        Args:
            filename: file to parse

        Returns:
            Boolean
        """
        parser = ConfigParser()
        # parser optionxform=str retains case
        parser.optionxform = str
        parser.read(filename)
        config_dict = dict(parser._sections)
        for key in config_dict:
            config_dict[key] = dict(parser._defaults, **config_dict[key])
            config_dict[key].pop('__name__', None)
            for param, value in config_dict[key].items():
                result = self.set(container=key, parameter=param, value=(value or "None"))
                if result is False:
                    return result
                else:
                    print('[+] {0} - {1}'.format(key, param))
        return True


@click.command()
@click.argument('filename', type=click.Path(exists=True))
@click.option('--namespace',
              prompt='Application Namespace',
              help='The application name')
@click.option('--env',
              prompt='Application Environment',
              help='The application environment (pilot, prod, etc..)')
def main(filename, namespace, env):
    """
    Main entrypoint for program
    """
    client = SMPSUploader(namespace, env)
    client.upload(filename)
