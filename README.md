# Search Indexing

This repository contains code for my personal search indexing experiments.

## What this project can do

This project has two parts:

1. A search index builder.
2. A query interface.

### Search index builder

The search index builder can:

1. Build a reverse search index from JSON objects.
2. Search the index for terms.
3. Return full records for a term.

### Query interface

To aid with experimentation, and to allow me to further explore search-as-you-type query interfaces, this project comes with a query interface.

The query interface accepts a plain text query and returns results from the search index for the given query.

## Getting Started

    To complete.

## Benchmarking

Thus far, this project has been used with small indexes (under 1,000 records). It takes around 7 seconds to build an index with 1,000 HTML documents and accompanying metadata. It takes less than 0.1 seconds to return results for a plain text query from this dataset.

## License

This project is licensed under the [MIT license](LICENSE.md).

## Contributors

- capjamesg