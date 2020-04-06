# Digital Marketplace Makefiles

Shared Makefiles for local development of Digital Marketplace apps.

## Installation

In the directory for the app run

    $ make -f ../digitalmarketplace-utils/Makefiles/include/makefiles.Makefile

Then edit the apps Makefile to read

    include Makefiles/frontend.Makefile

or

    include Makefiles/api.Makefile

as appropriate.

You should be able to then delete the rest of the Makefile!

To see what commands are available run

    make help

## Customising

If you want to do things a bit differently to other apps, you can include `Makefiles/common.Makefile` and then add commands as needed.
