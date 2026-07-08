# Joule Application Programming Interface (API)

!!! NOTE

    The Joule Application Programming Interface (API) uses asynchronous coroutines and must be run inside an event loop.
    To run the examples in this documentation interactively use the asyncio module:

    ``` bash title="Asyncio REPL"
    $> python3 -m asyncio
    asyncio REPL 3.X.X
    ...
    >>> import asyncio
    >>>
    ```

    A Jupyter Notebook that provides an overview of the API functionality is available from [GitHub](https://github.com/wattsworth/joule/blob/master/API_demo.ipynb). To run this notebook follow the commands below to install [Jupyter](https://jupyter.org/) and [matplotlib](https://matplotlib.org/), retrieve the notebook file, and start the Jupyter server:

    ``` {.bash .copy title="SHELL"}
    pip install jupyterlab matplotlib # prefix with sudo for system-wide install
    wget https://raw.githubusercontent.com/wattsworth/joule/master/API_demo.ipynb
    jupyter lab --ip=0.0.0.0 # add the --ip flag to allow external connections
    ```





## Joule Nodes
A `Node` represents a Joule instance and is the only means to access API methods. **Do not create manually create a Node object.** Instead, use [joule.api.get_node][] to create a connection to a specific node. Joule modules have a node object created automatically that refers to the Joule node running it.

```python title="Module Access"

# Inside a joule.client.ReaderModule class
async def run(self, parsed_args, output):
    node_info = await self.node.info()
    # other code ...
```
See [#working-with-nodes] for more information on managing access to Joule nodes using the API. These tools are also available through the CLI. 

The rest of this section describes class methods separated by category.

::: joule.api.BaseNode
    options:
        show_root_toc_entry: false
        docstring_section_style: table
        heading_level: 3


## Working with Nodes
::: joule.api
    options:
        show_root_toc_entry: false
        show_root_members_full_path: true
        heading_level: 3

``` python title="Asyncio REPL"
>>> import joule
>>> my_node = joule.api.get_node()
```


## API Models
::: joule.api.Folder
    options: 
        heading_level: 4
::: joule.api.EventStream
    options: 
            heading_level: 4
::: joule.api.EventStreamInfo
    options: 
            heading_level: 4
::: joule.api.DataStream
    options: 
            heading_level: 4
::: joule.api.DataStreamInfo
    options: 
            heading_level: 4
::: joule.api.Element
    options: 
            heading_level: 4
::: joule.api.Module
    options: 
            heading_level: 4
::: joule.api.ModuleStatistics
    options: 
            heading_level: 4
::: joule.api.Annotation
    options: 
            heading_level: 4

## API Exceptions
::: joule.errors.ApiError

## Utilities
::: joule.utilities
