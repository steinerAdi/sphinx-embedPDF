Embed PDF Documentation
=======================


New-Tab Links
-------------

To add a new-tab link, use the following code:

.. code-block:: rst

   :ntLink:`google <https://www.google.com>|true`
   or :ntLink:`https://www.google.com|true` 
   or :ntLink:`https://www.google.com` 
   or :ntLink:`https://www.google.com|false`.

Which results in: :ntLink:`google <https://www.google.com>|true` or :ntLink:`https://www.google.com|true` or :ntLink:`https://www.google.com` or :ntLink:`https://www.google.com|false`.


Download with Symbols
---------------------
To add a download from a file, use the following code:

.. code-block:: rst

   :download_file:`google <https://www.google.com>|true`
   or :download_file:`https://www.google.com|true` 
   or :download_file:`https://www.google.com` 
   or :download_file:`https://www.google.com|false`.

Which results in: :download_file:`sample.pdf <_static/sample.pdf>|true` 
or :download_file:`/_static/sample.pdf|true` 
or :download_file:`/_static/samples.pdf` 
or :download_file:`/_static/sample.pdf|false`.



Embed PDF
---------

PDF Page can be used to set a title including a download icon and new tab icon.

.. code-block:: rst

   .. embedpdf:: sample.pdf
      :alt: Alternative text to show pdf is not visible
      :name: Embed PDF Sample
      :width: 95
      :ratio: 75
      :hideheader:

Which results in:

.. embedpdf:: sample.pdf
   :alt: Alternative text to show pdf is not visible
   :name: Embed PDF Sample
   :width: 95
   :ratio: 75
   :hideheader:

Further features are in coming.

.. toctree:: 
   :hidden:
   :caption: Content

   gettingStarted.rst
   exampleCollection/index.rst
   faq.rst
