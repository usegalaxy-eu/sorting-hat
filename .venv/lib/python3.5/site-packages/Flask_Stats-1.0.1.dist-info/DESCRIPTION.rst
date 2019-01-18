===========
Flask-Stats
===========

This flask extension automatically provides paging timing and http status code
statistics to statsd.

It will send page timings to `<APP_NAME>.<BLUEPRINT>.<FUNCTION>`, and status
codes to `<APP_NAME>.<BLUEPRINT>.<FUNCTION>.http_XXX`, where XXX is the status
code, i.e 403.

Installation
------------

Install by installing it from the Python Package Index.

.. code-block:: console

    $ pip install Flask-Stats

Configuration
-------------

Flask-Stats uses the following configuration values.


=============================== ========================================================
`STATS_HOSTNAME`                Specifies the host to send statsd values to. Defaults to
                                localhost.
`STATS_PORT`                    Specified the port to send statsd values to. Defaults to
                                8125.
`STATS_BASE_KEY`                The base key to send the stats to. Defaults to the
                                application name.
=============================== ========================================================

Changelog
---------

1.0.0
~~~~~

- No longer reports timing values for endpoints that don't exist.

Todo
----

More functionality? What Would you like?


