# Joule Modules

Modules are executable programs that process data :ref:`sec-data-streams`. They are
connected to each other by :ref:`pipes`. Joule runs each module as a separate
process. This enforces isolation and improves resiliency.
Malfunctioning modules do not affect other parts of the pipeline
and can be restarted without interrupting the data flow. There are three basic types:
:ref:`sec-reader`, :ref:`sec-filter`, and :ref:`sec-composite`.

Examples in the documentation below are available at https://github.com/wattsworth/example-modules.git
This repository provides serveral examples of each module types and can be used as a template
to design your own installable Joule modules.


``` {.bash .copy title="SHELL"}
git clone https://github.com/wattsworth/example-modules.git
# install modules in the jouled virtual environment
cd example-modules
/opt/joule/bin/pip install .
```

The layout of the repository is shown below.

```
example_modules/
├── jouleexamples
│   ├── example_composite.py
│   ├── example_filter.py
│   ├── example_reader.py
│   └── ... other modules
├── module_configs
│   ├── example_composite.conf
│   ├── example_filter.conf
│   ├── example_reader.conf
│   └── ... other module configs
├── README.rst
└── stream_configs
    └── ... stream config examples
```

## Reader Modules

Reader modules are designed to read data into the Joule Framework. Data can come from
sensors, system logs, HTTP API's or any other timeseries data source. Reader modules
should extend the base class :class:`joule.client.ReaderModule` illustrated below.

![Reader Module](images/reader_module.png)


### Examples

#### Basic Reader

``` python title="example_reader.py"
--8<-- "jouleexamples/example_reader.py"
```


Reader modules should extend the base :class:`joule.client.ReaderModule` class. The
child class must implement the :meth:`joule.client.ReaderModule.run` coroutine which should perform
the following in a loop:

  1. Read data from the input
  2. Timestamp data with Unix microseconds
  3. Insert data into the output stream
  4. Sleep to create the data rate

Line 11 reads data from the input (a random number function). Line 12
timestamps the data and inserts it into the output stream. Line 13
sleeps for one second creating a 1Hz sample rate. Note that the
asyncio.sleep coroutine is used instead of the time.sleep function.


!!!NOTE
    The loop structure shown above should only be used for low bandwidth
    data sources. For higher bandwidth data pipe caching should be enabled or
    the data should be written in chunks as shown below. Write frequency should be 1Hz
    or lower to reduce inter-process communication and network overhead.


#### High Bandwidth Reader

``` python title="high_bandwidth_reader.py"
--8<-- "jouleexamples/high_bandwidth_reader.py"
```

Describe the argument parsing setup


#### Intermittent Reader

Another example showing how to handle sensor errors by creating intervals

``` python title="intermittent_reader.py"
--8<-- "jouleexamples/intermittent_reader.py"
```

### Development


During development it is often helpful to run the reader module as a standalone
process in order to use debuggers such as pdb or visualization tools like matplotlib.pyplot.
When a reader module is executed from the command line the output pipe is connected to stdout:

``` bash title="SHELL"
$>./demo_reader.py
1485188853650944 0.32359053067687582 0.70028608966895545
1485188853750944 0.72139550945715136 0.39218791387411422
1485188853850944 0.40728044378612194 0.26446072057019654
1485188853950944 0.61021957330250398 0.27359526775709841
# hit ctrl-c to stop
```

If the ``--module_config`` argument is specified the output pipe is instead connected to the stream specified in the configuration file. The stream will be created if it does not exist. By default the module will connect to the local
joule server, use the ``--url`` option to connect to a specific joule server. Any arguments in the configuration file will be parsed as if they were specified on the command line.

```bash title="SHELL"
$>./demo_reader.py --module_config=module.conf
  Contacting joule server at http://localhost:8080
# hit ctrl-c to stop
```

### Testing

This section refers to **test_reader.py** in the example_modules repository. Joule unittests are written using `asynctest
<https://asynctest.readthedocs.io/en/latest/>`_, a library built on top of the standard **unittest** module that reduces the boilerplate of writing tests for async coroutines.

Each unittest file should contain a single ``async.TestCase`` class. The
test runner will automatically run any functions starting with
``test_``. Each test should have a docstring explaining the input and desired output.
Tests should have three main sections as shown in the **test_reader** function below:

``` python
class TestReader(asynctest.TestCase):

    def test_reader(self):
        " with a rate=0.1, reader should generate 10 values in 1 second "
    # 1. build test objects
    # 2. run reader in an event loop
    # 3. check the results
```

#### Build test objects


``` python
# build test objects
my_reader = ReaderDemo()
pipe = LocalPipe("output", layout="float32_1")
args = argparse.Namespace(rate=0.1, pipes="unset")
```

1. Create an instance of the reader module. Properly designed readers
   should not require any initialization parameters.

2. Create an output pipe to receive data from the
   module. ``LocalPipe`` takes two arguments, a pipe name which
   should be a helpful string, and a layout. The layout should match
   the stream configuration file associated with your module. See the
   NumpyPipe documentation for details on local pipes and the layout
   parameter.

3. Create an args object that contains values for any custom arguments
   your module requires, it also should also initialize the pipes
   argument to "unset". In production, modules generate pipes
   automatically from their command line parameters. In testing we
   disable the pipe building routine by using the keyword "unset", and
   instead pass our own pipe to the module's run function, below.

#### Run event loop

``` python
loop = asyncio.get_event_loop()
my_task = asyncio.ensure_future(my_reader.run(args, pipe))
loop.call_later(1, my_task.cancel)
try:
    loop.run_until_complete(my_task)
except asyncio.CancelledError:
    pass
loop.close()
```

Modules are asynchronous coroutines that run in an event loop.  The
asynctest framework provides a new event loop for each test so we can
safely use the global loop returned by ``asyncio.get_event_loop``.
This code is common boilerplate for all reader modules and in
general it should not require any customization. The code does the following:

1. Get a reference to the global event loop
2. Set up the reader to run as a ``Task`` using the arguments and pipe created earlier
3. Schedule the reader task to be cancelled after one second
4. Run the event loop ``loop`` until the reader task stops
5. When the reader task is cancelled it generates a ``CancelledError`` which can be safely ignored
6. Close the event loop so the test exits cleanly


#### Check results

``` python
result = pipe.read_nowait()
# data should be 0,1,2,...,9
np.testing.assert_array_equal(result['data'],
                                        np.arange(10))
# timestamps should be about 0.1s apart
np.testing.assert_array_almost_equal(np.diff(result['timestamp'])/1e6,
                                                np.ones(9)*0.1, decimal=2)
```

This is the most important part of the test and it will vary greatly from module to module.
There are two steps:

1. Retrieve data from the pipe using ``pipe.read_nowait()``. This is
   the synchronous version of the ``read`` command and should only be
   used in testing. Modules should always use the ``await
   pipe.read()`` syntax.  By default ``read_nowait`` returns a
   structured array with a **data** field and **timestamp** field. If
   you want timestamps in column 0 and elements in columns 1-N, use
   ``read_nowait(flatten=True)``


2. Use the ``numpy.testing`` library to compare the data to an
   expected dataset you create manually.  Note that the
   ``assert_array_almost_equal`` is the preferred testing
   function. Floating point arithmetic is inexact so directly
   comparing data using ``==`` can generate spurious errors.



.. _ArgumentParser: https://docs.python.org/3/library/argparse.html#argparse.ArgumentParser
.. _Namespace: https://docs.python.org/3/library/argparse.html#argparse.Namespace

### Documentation

::: joule.client.ReaderModule
    options:
        show_root_toc_entry: false
        heading_level: 4
        inherited_members: true


## Filter Modules


Filter modules process data. They may have one or more input streams and one or
more output streams. Filter modules should extend the base class :class:`joule.client.FilterModule` illustrated below.

![Filter Module](images/filter_module.png)


### Examples


#### Basic Filter


``` python title="example_filter.py"
--8<-- "jouleexamples/example_filter.py"
```

Filter modules should extend the base :class:`FilterModule` class. The
child class must implement the :meth:`joule.FilterModule.run` coroutine which should perform
the following in a loop:

  1. Read from input pipe(s)
  2. Perform data processing
  3. Write to output pipe(s)
  4. Consume input data

Lines 10-11 retrieve the module's :class:`joule.Pipe` connections to the
input and output streams. Line 19 reads in new data from the "raw" stream into a
Numpy `structured array`_. Line 21 applies the linear scaling to the data in place.
The data is then written to the output pipe in line 23 and the input data is removed
from the buffer on line 25. The sleep statement ensures that data is processed in large
chunks regardless of the rate at which it arrives. This ensures the system operates efficiently
by reducing the frequency of context switches and inter-process communication.


#### Offset Filter

``` python title="offset_filter.py"
--8<-- "jouleexamples/offset_filter.py"
```

The loop executes a WINDOW size median filter. Line 16 reads in new data from the “raw” stream into a
[structured array](https://docs.scipy.org/doc/numpy-1.13.0/user/basics.rec.html). Lines 19-20 execute the median filter in place. Many filtering algorithms including
median require data before and after a sample to compute the output. Modules process data in chunks
which produces artifacts at the beginning and end where there is insufficient data to compute the output.
In this instance, the first and last EDGE samples of the chunk are invalid so they are omitted from the
output in Line 23. The call to consume() on Line 26 prepends the last 2 × EDGE samples to the next input
chunk to compensate for these boundary artifacts. This execution sequence produces exactly the same
result as a median filter run over the entire dataset at once.


### Development


During development it is often helpful to run modules as standalone
processes in order to use debuggers such as pdb or visualization tools like matplotlib.pyplot.
Filter (and Composite) modules may be executed outside of the Joule environment in
either **live** or **historic** mode. When executed independently the module configuration
file must be provided so that the module can request the appropriate stream connections from
Joule.

!!! NOTE
    The joule service must be running in order to run filters as standalone processes


**Live Isolation**
Connect filter inputs to live streams produced by the current joule pipeline.
Specify the module configuration file and a directory with configurations
for each output stream.

``` bash title="SHELL"
# [module.conf] is a module configuration file
$>./demo_filter.py --module_config=module.conf
Requesting live stream connections from jouled... [OK]
#...stdout/stderr output from filter
# hit ctrl-c to stop
```

**Historic Isolation**
Connect filter inputs to a range of stream data saved in NilmDB.

Specify historic execution by including a time range with **--start**
and **--end** arguments. The time range may be a date
string or a Unix microseconds timestamp. Common phrases are also supported
such as "2 hours ago" or "today".

!!! WARNING
    Running a filter in historic isolation mode will overwrite
    existing output stream data

``` bash title="SHELL"
# [module.conf] is a module configuration file

$>./demo_filter.py --module_config=module.conf \
        --start="yesterday" --end="1 hour ago"
    Requesting historic stream connections from jouled... [OK]
#...stdout/stderr output from filter</i>

# program exits after time range is processed
```

### Testing

TODO

### Reference

::: joule.client.FilterModule
    options:
        show_root_toc_entry: false
        heading_level: 4
        inherited_members: true

## Composite Modules

Composite modules aggregate multiple modules into a single
process. They may have one or more input streams and one or
more output streams. Composite modules should extend the base
class :class:`joule.client.CompositeModule` illustrated below.

![Composite Module](/images/composite_module.png)

#### Examples


``` python title="example_composite.py"
--8<-- "jouleexamples/example_composite.py"
```

The child class must implement the :meth:`joule.CompositeModule.setup` coroutine
which should perform the following:

  1. Create modules
  2. Create local pipes for interior streams
  3. Start modules by calling :meth:`joule.BaseModule.run` with the appropriate parameters
  4. Return module tasks for execution in the main event loop

This example contains a :ref:`sec-high-bandwidth-reader` connected to a :ref:`sec-median-filter`.
The modules are connected with a :class:`joule.LocalPipe` and the output of the
filter is connected to a :class:`joule.OutputPipe` named **filtered**.

Creating Module Arguments
  In the example above, both modules receive the **parsed_args** parameter directly.
  In more complex scenarios it is often necessary to construct a :class:`argparse.Namespace` object
  for each module with the particular arguments it requires. Make sure *all* arguments are specified
  and match the expected data types The code snipped below constructs an appropriate Namespace
  object for the ArgumentParser configuration.

``` python title="Handling Command Line Arguments"

import json
import argparse

# example ArgumentParser

args = argparse.ArgumentParser("demo")
args.add_argument("--arg1", required=True)  # modules should use keyword arguments
args.add_argument("--arg2", type=int, required=True)
args.add_argument("--arg3", type=json.loads, required=True)

# to produce these arguments manually:

module_args = argparse.Namespace(**{
"arg1": "a string",  # type not specified
"arg2": 100,         # type=int
"arg3": [100,10,4]   # type=json
})
```


### Development

See Filter Development

### Testing


See Filter Testing

### Reference


::: joule.client.CompositeModule
    options:
        show_root_toc_entry: false
        heading_level: 4
        inherited_members: true

## User Interfaces
Modules can provide web-based user interfaces.
When a Joule node is connected to
a Lumen server, the user authentication and authorization is handled
by Lumen and the interface is presented on a common dashboard with other
modules the user is authorized to use.

To add an interface to a module implement the :meth:`joule.client.BaseModule.routes` function
and register handlers for any routes your module implements. Then enable the interface
by changing the ``is_app`` attribute to ``yes`` in the
:ref:`sec-modules` file.

### Examples

#### Basic Interface

``` python title="example_interface.py"
--8<-- "jouleexamples/example_interface.py"
```

#### Bootstrap Interface

Typical web interfaces require more complex HTML, cascading style sheets (CSS), and javascript. The example below
provides a complete module implementation using the `Bootstrap <http://getbootstrap.com/>`_ CSS framework
and `Jinja <http://jinja.pocoo.org/>`_ HTML templates.

``` python title="bootstrap_composite.py"
--8<-- "jouleexamples/bootstrap_interface.py"
```

In addition to the module code itself this interface requires several additional files located in the assets directory
as shown:

``` title="file layout"
├── bootstrap_interface.py
└── assets
    ├── css
    │   └── main.css # and other css files
    ├── js
    │   └── index.js # other js files
    └── templates
        ├── layout.jinja2
        └── index.jinja2
```

The HTML templates are stored in ``assets/templates``. **layout.jinja2** is common to all views and provides hooks
to customize the content and inject additional stylesheet and script tags. The module home page renders **index.jinja**
which is shown below:

``` jinja title="assets/templates/index.jinja2"
--8<-- "jouleexamples/assets/templates/index.jinja2"
```

Notice that additional CSS and javascript assets that are injected into the appropriate blocks in the layout template.
Bootstrap classes provide a simple and powerful mechanism for creating a basic page, but in some cases it may be
necessary to add custom CSS to fine tune an element's appearance.

``` css title="assets/css/index.css"
--8<-- "jouleexamples/assets/css/index.css"
```

Javascript makes websites interactive. This file makes repeated calls to the server for new data.
Using AJAX requests rather than reloading the entire page improves the user's experience and reduces network traffic.

``` javascript title="assets/js/index.js"
--8<-- "jouleexamples/assets/js/index.js"
```

#### Development

When running as a standalone process, modules that provide a web interface
will start a local webserver on port 8000 (by default). This is accessible
from a browser at ``http://localhost:8000``.