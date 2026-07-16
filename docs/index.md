---
hide:
  - navigation   # Hides the left-hand sidebar navigation on the home page
  - toc          # Hides the right-hand table of contents on the home page
---

<div class="custom-hero" markdown>
  <div class="header-container">
    <img alt="logo" class="header-img" src="../images/logo.png"> 
    <h1>Wattsworth</h1>
  </div>
  <h2>A Decentralized IoT Framework</h2>
  <h3> acquire, process, and visualize data across distributed nodes</h3>
  <div class="hero-buttons" markdown>
  
  [Get Started](installation.md){: .md-button .md-button--primary}

  [Learn More](overview.md){: .md-button .md-button--primary}

  </div>

  <div class="hero-corner-links" markdown>
  
  [license](about.md#license) | 
  <a href="https://github.com/wattsworth" aria-label="View source on GitHub" target="_blank" rel="noopener" > 
    :fontawesome-brands-github:
  </a>
  </div>
</div>

<div class="grid cards" markdown>

-   :fontawesome-solid-microchip:{ .lg .middle } __Data Acquisition__

    ---

    Ingest data using builtin tools or create reader modules to 
    interface with custom sensors or API's. Designed for long term data storage
    and data rates from sub-Hz to KHz.


    [:fontawesome-solid-angle-right: Reader Modules](module_development.md#reader-modules)
    
    [:fontawesome-solid-angle-right: Command Line Interface](cli.md)

-   :fontawesome-solid-magnifying-glass-chart:{ .lg .middle } __Data Processing__

    ---

    Process and analyze data ad-hoc using the Python API or incoporate realtime
    analysis into your data pipeline with filter modules. Export data to other tools using CSV and [HDF](https://www.hdfgroup.org/solutions/hdf5/).

    [:fontawesome-solid-angle-right: Filter Modules](module_development.md#filter-modules)

    [:fontawesome-solid-angle-right: Python API](api.md)


-   :fontawesome-solid-display:{ .lg .middle } __Data Visualization__

    ---

    A web platform provides interactive access to time series and event data. Can be run locally or deploy to the cloud. Customize the platform with Reader and Filter module interfaces. 

    [:fontawesome-solid-angle-right: Module Interfaces](module_development.md#user-interfaces)

    [:fontawesome-solid-angle-right: Web Platform](lumen/explorer.md)

    



    
</div>
