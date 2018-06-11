# README

## Directory tree layout

* `freenodejobs/`

  This directory contians the [Django](https://www.djangoproject.com/) project for this. It makes use of nested [applications](https://docs.djangoproject.com/en/2.0/ref/applications/) to organise the code.

* `freenodejobs/settings/`

  This directory contains the distributable [Django settings](https://docs.djangoproject.com/en/2.0/ref/settings/) for the project. The majority of the settings are stored in `defaults/*.py` and then "roles" are applied on top of this to override them when running outside of production and/or in tests controlled by the `role.py` file that is overridden by the deployment. For local settings to your personal environment. you can add them to the `freenodejobs/settings/custom.py` file.

* `media/`

  This directory contains assets that will are served publically via Nginx. They are managed by the [Django staticfiles mechanism](https://docs.djangoproject.com/en/2.0/ref/contrib/staticfiles/) with the addition of the [`django-staticfiles-dotd`](https://chris-lamb.co.uk/projects/django-staticfiles-dotd) third-party application to automatically concatenate `foo.ext.d` directories (into a `foo.ext` file) and to render `.scss` ([Sass](https://sass-lang.com/)) files via the `STATICFILES_DOTD_RENDER_PIPELINE` setting.

* `templates/`

  Contains regular [Django templates](https://docs.djangoproject.com/en/2.0/topics/templates/). organised by application.

* `data/`

  This directory contains files that should be available to the Django project but not available via the web server (c.f. `static/`).

* `config/`

  Contains [Ansible](https://www.ansible.com/) roles, etc. for deploying the site. Called via `.travis.yml`, the main script is at `deploy/entry`  which expects a `ANSIBLE_VAULT_PASSWORD` variable to be exported to the environment (set in the private [Travis CI](https://travis-ci.org/) settings, but also available in [Lastpass](https://www.lastpass.com/)) in order to decrypt private data such as SSH keys, AWS keys, Django's [`SECRET_KEY`](https://docs.djangoproject.com/en/2.0/ref/settings/#std:setting-SECRET_KEY), etc.

* `debian/`

  As part of the deployment pipeline, a Debian `.deb` package is built using [dh-virtualenv](http://dh-virtualenv.readthedocs.io) to ensure a tidy installation on the target server. The [Gunicorn](http://gunicorn.org/) WSGI server is started via the [systemd](https://www.freedesktop.org/software/systemd/man/systemd.service.html) `debian/freenodejobs.freenodejobs-gunicorn.service` file.


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
