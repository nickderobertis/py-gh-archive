Getting started with gharchive
**********************************

Install
=======

Install via::

    pip install gharchive


Or, for multi-processing in extracting archives::

    pip install gharchive[mgzip]

Usage
=========

This is a simple example::

    from gharchive import GHArchive
    gh = GHArchive()

    data = gh.get('6/8/2020', '6/10/2020', filters=[
        ('repo.name', 'bitcoin/bitcoin'),
        ('type', 'WatchEvent')
    ])


