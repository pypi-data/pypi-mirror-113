Welcome to Entity Embed's documentation!
========================================

Release v\ |version|.

Entity Embed allows you to transform entities like companies, products, etc. into vectors to support **scalable Record Linkage / Entity Resolution using Approximate Nearest Neighbors**.

Using Entity Embed, you can train a deep learning model to transform records into vectors in an N-dimensional embedding space. Thanks to a contrastive loss, those vectors are organized to keep similar records close and dissimilar records far apart in this embedding space. Embedding records enables `scalable ANN search <http://ann-benchmarks.com/index.html>`_, which means finding thousands of candidate duplicate pairs of records per second per CPU.

Entity Embed achieves Recall of ~0.99 with Pair-Entity ratio below 100 on a variety of datasets. **Entity Embed aims for high recall at the expense of precision. Therefore, this library is suited for the Blocking/Indexing stage of an Entity Resolution pipeline.**  A scalabale and noise-tolerant Blocking procedure is often the main bottleneck for performance and quality on Entity Resolution pipelines, so this library aims to solve that. Note the ANN search on embedded records returns several candidate pairs that must be filtered to find the best matching pairs, possibly with a pairwise classifier (the Record Linkage example includes that).

Entity Embed is based on and is a special case of the `AutoBlock model described by Amazon <https://www.amazon.science/publications/autoblock-a-hands-off-blocking-framework-for-entity-matching>`_.

.. toctree::
   :maxdepth: 2
   :caption: User Guide

   guide/install
   guide/usage
   guide/field_types
   guide/nn_architecture
   guide/cli

.. toctree::
   :maxdepth: 1
   :caption: Developer Documentation

   dev/contributing
   dev/release_process
   dev/authors

.. toctree::
   :maxdepth: 1
   :caption: Releases

   changelog
