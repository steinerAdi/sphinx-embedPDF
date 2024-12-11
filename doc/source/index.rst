Embed PDF test documentation
============================

To add a new-tab link, use the following code:

.. code-block:: rst

   :ntLink:`src:https://www.google.com, name:google, symbol:1`

Which results in: :ntLink:`src:https://www.google.com, name:google, symbol:1`.

PDF Page can be used to set a title including a download icon and new tab icon

.. code-block:: rst

   .. embedpdf:: ./_static/sample.pdf
      :alt: Alternative text to show pdf is not visible
      :name: Embed PDF Sample
      :width: 95
      :ratio: 75
      :hideheader:

Which results in:

.. embedpdf:: ./_static/sample.pdf
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
