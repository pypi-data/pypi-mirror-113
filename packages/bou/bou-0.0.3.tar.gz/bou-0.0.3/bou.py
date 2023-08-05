#!/usr/bin/env python3
import os
import re
import sys
from argparse import ArgumentParser
from pathlib import Path
from subprocess import Popen, PIPE, STDOUT

import yaml

BUILD_FILES = ['build.yaml', 'build.yml', 'bou.yaml', 'bou.yml']
ENV_VAR = re.compile(r'(\$([A-Za-z0-9_]+))')


class StepFailedError(Exception):
    pass


def parse_args():
    """
    Parse command line arguments, and return an object with all the arguments

    :return: A namespace object with all the supplied arguments
    """
    parser = ArgumentParser()
    parser.add_argument('-f', '--file', dest='build_file', help='Path to the build file')
    parser.add_argument('stage_or_step', nargs='?', default=None, help='Run a particular stage or step')
    return parser.parse_args()


def setup_env(env, base_path):
    """
    Set up the environment dictionary, resolving shell variables

    :param env: The environment list or dictionary
    :param base_path: The base path that the build runs in

    :return: A merged dictionary of environment variables
    """
    if isinstance(env, list):
        env = {pair.split('=')[0]: pair.split('=')[1] for pair in env}
    env = dict(BASE_DIR=str(base_path), **env)
    for key, value in env.items():
        match = ENV_VAR.search(value)
        if match:
            value = value.replace(match.group(1), env[match.group(2)])
            env[key] = value
    return dict(**os.environ, **env)


def setup_step(config, step_name):
    """
    Prepare a step for usage

    :param config: The build configuration
    :param step_name: The name of the step to prepare

    :return: A step object
    """
    step = config['steps'][step_name]
    step['environment'] = config.get('environment', []) + step.get('environment', [])
    step['name'] = step_name
    return step


def get_steps_for_stage(config, stage_name):
    """
    Get all the steps for a particular stage

    :param config: The build configuration
    :param stage_name: The name of the stage

    :return: A list of step objects
    """
    steps = []
    for step_name in config['steps'].keys():
        if config['steps'][step_name]['stage'] == stage_name:
            steps.append(setup_step(config, step_name))
    return steps


def run_step(step, base_path):
    """
    Run a particular step

    :param step: The step (as a dictionary)
    :param base_path: The base path to run this in

    :return: Return True if the step passed, or False if the step failed
    """
    script = step['script']
    if isinstance(script, list):
        script = os.linesep.join(script)
    env = setup_env(step['environment'], base_path)
    proc = Popen([script], shell=True, stdout=PIPE, stderr=STDOUT, env=env)
    for output in iter(lambda: proc.stdout.read(1), b''):
        sys.stdout.buffer.write(output)
        sys.stdout.buffer.flush()
    proc.stdout.close()
    proc.wait()
    return not proc.returncode


def run_stage(config, stage_name, base_path):
    """
    Run all the steps in a particular stage

    :param config: The build configuration
    :param stage_name: The stage to run
    :param base_path: The base path of the build
    """
    steps = get_steps_for_stage(config, stage_name)
    for step in steps:
        result = run_step(step, base_path)
        if not result:
            raise StepFailedError('Error running step "{name}"'.format(name=step['name']))


def get_all_stages(config):
    """
    Return all the stages available in the build configuration

    :param config: The build configuration

    :return: A list of stages
    """
    stages = config.get('stages', [])
    for step_name, step in config['steps'].items():
        if step['stage'] not in stages:
            stages.append(step['stage'])
    return stages


def get_all_steps(config):
    """
    Return all the steps available in the build configuration

    :param config: The build configuration

    :return: A list of steps
    """
    return list(config.get('steps', {}).keys())


def get_build_file():
    """
    Determine the local build file
    """
    base_path = Path.cwd()
    for child in base_path.iterdir():
        if child.name in BUILD_FILES:
            return child.resolve()
    return None


def main():
    """
    Run the build system
    """
    args = parse_args()
    if args.build_file:
        build_file = Path(args.build_file).resolve()
    else:
        build_file = get_build_file()
    if not build_file:
        print('Could not find a valid build file')
        return 1
    base_path = build_file.parent
    config = yaml.full_load(build_file.open())
    all_stages = get_all_stages(config)
    all_steps = get_all_steps(config)
    try:
        if args.stage_or_step:
            if args.stage_or_step in all_stages:
                run_stage(config, args.stage_or_step, base_path)
            elif args.stage_or_step in all_steps:
                step = setup_step(config, args.stage_or_step)
                run_step(config, step, base_path)
            else:
                print('"{stage}" is not a valid stage or step name'.format(stage=args.stage_or_step))
                return 2
        else:
            stages = config.get('stages', all_stages)
            if stages:
                for stage_name in stages:
                    run_stage(config, stage_name, base_path)
            else:
                for step_name in all_steps:
                    step = setup_step(config, step_name)
                    run_step(config, step, base_path)
    except StepFailedError as e:
        print(str(e))
        return 3
    return 0


if __name__ == '__main__':
    sys.exit(main())
