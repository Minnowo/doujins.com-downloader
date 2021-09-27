doujinsDotcom
=======

.. code-block::

     _____                             
    |     \  ___  _   _ _____ _          
    |  /\  |  _ \| | | |__   (_)_ ___  ____    ____  ___  __  __
    | (  ) | / \ | | | |_ | || | `_  \/  __\  |   _|/ _ \/  \/  \  
    |  \/  | \_/ | |_/ | \| || | | | |/\_  \ _|  (_| |_| | |\/| |
    |_____/ \___/ \__/\|\___/|_|_| |_|\___ /|_|____|\___/|_|  |_|




doujinsDotcom is a CLI tool for downloading doujinshi from <http://doujins.com>

this is a modified copy of <https://github.com/Minnowo/nhentai-downloader>

which is based on <https://github.com/RicterZ/nhentai>

===================
Manual Installation
===================
.. code-block::

    git clone https://github.com/Minnowo/doujins.com-downloader
    cd nhentai
    python setup.py install




=====
Usage
=====

*The default download folder will be the path where you run the command + '/downloads/' (CLI path).*


Download specified doujinshi:

.. code-block:: bash

    nhentai --url=https://doujins.com/doujins-original-series/doushoku-54755,https://doujins.com/kantai-collection/taihou-s-deep-sea-fall-51641 -d
    or
    nhentai --url https://doujins.com/kantai-collection/taihou-s-deep-sea-fall-51641 --download
    or
    nhentai --file doujin.txt -d


Format output doujinshi folder name:

.. code-block:: bash

    nhentai--url https://doujins.com/kantai-collection/taihou-s-deep-sea-fall-51641 --download --format %p

Supported doujinshi folder formatter:

- %t: Doujinshi name
- %a: Doujinshi authors' name
- %p: Doujinshi pretty name


