# README

## Local database setup

1. Create PostgreSQL user with an id matching your UNIX username:

    ```
    $ sudo -u postgres createuser $(whoami) -SDR
    ```

2. Create a database owned by this user:

    ```
    $ sudo -u postgres createdb -E UTF-8 -O $(whoami) freenodejobs
    ```

3. Check we can connect to this database:

    ```
    $ /usr/bin/psql freenodejobs
    ```

4. Create empty tables, etc.:

    ```
    $ ./manage.py migrate
    ```

## Running the tests

```
./setup.py test
```

## Logs

https://eu-west-2.console.aws.amazon.com/cloudwatch/home?region=eu-west-2#logEventViewer:group=freenodejobs;stream=freenodejobs
