# Digital Marketplace Makefiles

Shared Makefiles for local development of Digital Marketplace apps.

## Installation

In the directory for the app run

    $ make \
        -f ../digitalmarketplace-utils/Makefiles/makefiles.Makefile \
        update-makefile \
        MAKEFILE_NAME=Makefiles/<app type>.Makefile

Replace app type with 'frontend' or 'api' as appropriate.

## Keeping Makefiles up to date

If you have merged changes to the main branch in this repo, you can update the
Makefile in each app by simply running

    $ make update-makefile

in the directory for each app.
