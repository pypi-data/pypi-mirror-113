bou
===

Bou (pronounced "bow") is a simple builder or task runner which uses a YAML file for task configuration.

Bou uses the concept of *stages* and *steps*. A stage is a sets of steps, and a step is a set of commands to run. A
stage can contain many steps, but a step can only belong to a single stage.

"Bou" is `Afrikaans`_ for "build".

Installation
------------

Install bou with pip:

.. code-block::

   $ pip install bou

Running bou
-----------

To run bou, simply run the command. The build file will be automatically detected.

.. code-block::

   $ bou

To specify a build configuration file, use the ``-f`` option.

.. code-block::

   $ bou -f /path/to/build.yaml

To specify a stage or a step to run, just add it to the command. Stages take priority over steps, so if you have a
stage and a step with the same name, the stage will be run.

.. code-block::

   $ bou build
   $ bou test


Task Configuration
------------------

When run without any parameters, bou will search for a file named ``bou.yaml``, ``bou.yml``, ``build.yaml`` or ``build.yml``

Here's a basic example:

.. code-block:: yaml

   stages:
     - build
     - test
   steps:
     build:
       stage: build
       script:
         - make
     test:
       stage: test
       script:
         - make test


Environment Variables
---------------------

Bou also supports setting environment variables, both at a global level, as well as at a step level. As a convenience,
bou sets up an initial environment variable named ``BASE_DIR`` which is the directory the build file is in.

Environment variables defined at a global level are set first when a step is run, and then the step-level environment
variables are set.

.. code-block:: yaml

   stages:
     - build
   environment:
     - PYTHON=python3
   steps:
     build:
       stage: build
       environment:
         - SOURCE=$BASE_DIR/src
       script:
         - $PYTHON $SOURCE/setup.py build


Stages and Steps
----------------

If no steps or stages are specified, by default bou will attempt to run the following, in order:

 1. All of the stages in the ``stages`` section of the task configuration
 2. If no stages are specified in the task config, all of the stages discovered in the steps
 3. If no stages are found, all of the steps


Source Code
-----------

The source code to bou is available on my personal Git server: https://git.snyman.info/raoul/bou


Copyright (c) 2021 Raoul Snyman

.. _Afrikaans: https://en.wikipedia.org/wiki/Afrikaans
