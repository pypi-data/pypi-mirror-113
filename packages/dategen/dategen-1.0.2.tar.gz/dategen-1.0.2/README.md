
# Table of Contents

1.  [Install](#org432e4c0)
2.  [Usage](#orge8bd4cf)
3.  [folder structures](#org5bdbbcc)

Dategen is a python package that yield a generator of dates.


<a id="org432e4c0"></a>

# Install

    $ python3 -m pip install dategen


<a id="orge8bd4cf"></a>

# Usage

    import dategen
    g = dategen.dategen.backward
    help(g)

    x=g()

    # only the last command will be displayed.
    
    # type( x )  # generator
    
    # list( x )  # 5000 datetime, a very long list.
    
    # next( x )  # one datetime form the generator
    
    # len( list(x) )  # 5000


<a id="org5bdbbcc"></a>

# folder structures

    
    date
    
    tree

    Fri Jul 23 17:57:13 CST 2021
     .
     ├── LICENSE
     ├── Pipfile
     ├── Pipfile.lock
     ├── README.md
     ├── Untitled.ipynb
     ├── Untitled1.ipynb
     ├── dategen
     │   ├── __init__.py
     │   └── dategen.py
     ├── log.org
     ├── pyproject.toml
     └── tests
         └── dategen.ipynb

