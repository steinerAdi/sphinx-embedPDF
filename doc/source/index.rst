Embed PDF test documentation
============================

To add a new-tab link, use the following code:

.. code-block:: rst

   :ntLink:`src:https://www.google.com, name:google, symbol:True`

Which results in: :ntLink:`src:https://www.google.com, name:google, symbol:True`.

PDF Page can be used to set a title including a download icon and new tab icon

.. code-block:: rst

   .. embedPDF:: /_static/sample.pdf

Which results in:

.. embedpdf:: /_static/sample.pdf
   :alt: Alternative text to show pdf is not visible

