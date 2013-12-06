.. nuit-info-2013-gos14 documentation master file, created by
   sphinx-quickstart on Fri Dec  6 07:19:39 2013.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Nuit de l'info 2013 - Équipe GOS14
==================================

Ceci est la documentation du projet de l'équipe GOS14 pour la nuit de l'info 2013. 

Introduction
------------

Nous avons décomposé notre projet en trois différentes applications:

* `Android <https://github.com/laza1618/android_dashboard>`_
* `iOS <https://github.com/SebastienFCT/Y-mobile>`_
* `Web côté serveur (en Python) <https://github.com/arnaudchenyensu/nuit-info-2013>`_

L'application Android
---------------------

Cette application communique avec le serveur Python, elle rentre dans le cadre du `défi tableau de bord <http://www.nuitdelinfo.com/nuitinfo/defis:tableau_de_bord:start>`_. Cette application correspond à la continuation de l'application web du serveur. Avec cette application, l'utilisateur peut prendre des photos, uploadées sur le serveur et le serveur répond en envoyant des mots clés, liens, etc.


L'application iOS
-----------------

Cette application pose à l'utilisateur des questions et ainsi identifie précisément le besoin de l'utilisateur et lui propose des réponses pour le moins originales. Elle est optimisée pour l'iPhone 5.

L'application web (en Python)
-----------------------------

C'est la base même de notre architecture. Nous avons décidé d'utiliser Python version 2.7. Afin de nous assurer du bon développement de l'application, nous avons utilisé différents outils:

* `virtualenv <https://pypi.python.org/pypi/virtualenv>`_ et `virtualenvwrapper <https://pypi.python.org/pypi/virtualenvwrapper>`_
* `pip <https://pypi.python.org/pypi/pip>`_ et `easy_install <https://pypi.python.org/pypi/setuptools>`_
* `Flask framework <http://flask.pocoo.org/>`_ (et ses `différentes extensions <http://flask.pocoo.org/extensions/>`_ : wtf, sqlalchemy...)
* `requests <http://requests.readthedocs.org/en/latest/>`_
* `sphinx <http://sphinx-doc.org/>`_ et `Read the Docs <https://readthedocs.org/>`_ (pour la documentation)

Nous avons décidé d'utiliser le web framework Flask a la place du plus populaire framework `Django <https://www.djangoproject.com/>`_ car nous l'avons trouvé plus simple d'utilisation et donc plus approprié pour la nuit de l'info.

Documentation API
-----------------

.. toctree::
   :maxdepth: 1

   api/database.rst
   api/gos14.rst
   api/models.rst

