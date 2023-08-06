sc-deploy-db
===============

sc-deploy-db is a multi-platform command line tool for deploying scripts to Snowflake

Installation
------------

.. code:: bash

    $ pip install snowconvert-deploy-tool --upgrade
    
.. note:: If you run this command on MacOS change `pip` by `pip3`


Usage
-----

.. code:: bash

    $ sc-deploy-db -h


For general help content, pass in the ``-h`` parameter:

.. code:: bash

    usage: sc-deploy-db [-h] [-A ACCOUNT] [-D DATABASE] [-WH WAREHOUSE] [-R ROLE]
                        -U USER -P PASSWORD [-W WORKSPACE] -I INPATH [-L LOGPATH]
                        [--SplitPattern SPLITPATTERN] [--ObjectType [OBJECTTYPE]]

        SnowConvertStudio Deployment Script
        ===================================

        This script helps you to deploy a collection of .sql files to a Snowflake Account.

        The tool will look for settings like:
        - Snowflake Account
        - Snowflake Warehouse
        - Snowflake Role
        - Snowflake Database

        If the tool can find a config_snowsql.ini file in the current directory or in the workspace\config_snowsql.ini location
        it will read those parameters from there.

::

    optional arguments:
      -h, --help            show this help message and exit
      -A ACCOUNT, --Account ACCOUNT
                            Snowflake Account
      -D DATABASE, --Database DATABASE
                            Snowflake Database
      -WH WAREHOUSE, --Warehouse WAREHOUSE
                            Snowflake Warehouse
      -R ROLE, --Role ROLE  Snowflake Role
      -U USER, --User USER  Snowflake User
      -P PASSWORD, --Password PASSWORD
                            Password
      -W WORKSPACE, --Workspace WORKSPACE
                            Path for workspace root. Defaults to current dir
      -I INPATH, --InPath INPATH
                            Path for SQL scripts
      -L LOGPATH, --LogPath LOGPATH
                            Path for process logs. Defaults to current dir
      --SplitPattern SPLITPATTERN
                            When provided it should be Regex Pattern to use to
                            split scripts. Use capture groups to keep separator.
                            For example: (CREATE OR REPLACE)
      --ObjectType [OBJECTTYPE]
                            Object Type to deploy
                            table,view,procedure,function,macro
      --authenticator [method]
                            When provided allow to use other authenticators for example 'externalbrowser'
      optional arguments:
      -h, --help    show this help message and exit

This tool assumes :

- that you have a collection of `.sql` files under a directory. It will then execute all those `.sql` files connecting to the specified database.
- that each file contains **only** one statement. 

.. note::  If your files contains several statements you can use the Split and SplitPattern arguments, so the tool will try to split the statements prior to execution.

Examples
--------

If you have a folder structure like:

::

    + code
       + procs
         proc1.sql
       + tables
         table1.sql
         + folder1
             table2.sql

You can deploy then by running:

::

    sc-deploy-db -A my_sf_account -WH my_wh -U user -P password -I code

If you want to use another authentication like Azure AD you can do:

::

    sc-deploy-db -A my_sf_account -WH my_wh -U user -I code --authenticator externalbrowser



Reporting issues and feedback
-----------------------------

If you encounter any bugs with the tool please file an issue in the
`Issues`_ section of our GitHub repo.


License
-------

sc-deploy-db is licensed under the `MIT license`_.


.. _Issues: https://github.com/MobilizeNet/SnowConvert_Support_Library/issues
.. _MIT license: https://github.com/MobilizeNet/SnowConvert_Support_Library/tools/snowconvert-deploy/LICENSE.txt
