# gutenparse

This project has a few parts, all of which are designed to help me curate the Labelled and Balanced Gutenberg Bookset (LABGUB).

1. `gutenparse.py`

    A little library to parse some common metadata from RDF metadata files in Project Gutenberg books.

2. `remove_*.py` scripts

    Several scripts to prune books from a collection of Project Gutenberg books.
    For these to work, it is assumed that the book collection is structured like so:

    ```
    collection
    ├── 9043
    │   ├── pg9043.rdf
    │   └── pg9043.txt.utf8
    ├── 9044
    │   ├── pg9044.rdf
    │   └── pg9044.txt.utf8
    ├── 9045
    │   ├── pg9045.rdf
    │   └── pg9045.txt.utf8
    ├── 9046
    │   ├── pg9046.rdf
    │   └── pg9046.txt.utf8
    └── 9047
        ├── pg9047.rdf
        └── pg9047.txt.utf8
    ```

    They are used by passing the RDF files as command line arguments.
    The results are logged in detail.

    ```bash
    $ python remove_non_english.py collection/*/*.rdf
    Processing 60 meta files...

    Removing SA /mnt/c/Users/kdbanman/Dev/gutenparse/tiny/9000
    Removing DE /mnt/c/Users/kdbanman/Dev/gutenparse/tiny/9046
    Removing DE /mnt/c/Users/kdbanman/Dev/gutenparse/tiny/9049
    Removing FR /mnt/c/Users/kdbanman/Dev/gutenparse/tiny/9053
    Removing DE /mnt/c/Users/kdbanman/Dev/gutenparse/tiny/9058
    Removing DE /mnt/c/Users/kdbanman/Dev/gutenparse/tiny/9066
    Removing FI /mnt/c/Users/kdbanman/Dev/gutenparse/tiny/9082
    Removing DE /mnt/c/Users/kdbanman/Dev/gutenparse/tiny/9083

    Non-English languages encountered during removal:
    DE (5)
    FI (1)
    SA (1)
    FR (1)

    Removed 8 books.
    ```

    _These scripts are destructive, and you are responsible for your own backups_.
    If you're scared, pass `--dry` as the _last_ parameter to do a dry run where nothing is actually deleted.

    ```bash
    $ python remove_multiple_authors.py collection/*/*.rdf --dry
    ```

3. `aggregate_stats.py`

    A final analysis script designed to log some aggregate stats and save a CSV containing labels for each book.


## TODO

- balance lcc subjects
  - _could_ get clever
    - parse out single letters. might not need to, or might be a bad idea. (currently doing this though)
    - remove specifics. (EX: E456)
  - might be best to just leave codes as-is and
    - remove under-represented
    - trim over-represented

- balance author birth years
  - don't need to get perfect uniform distribution over years
  - must truncate distribution tails
  - might need to trim over-represented decades

- license and headers

- perform prune and balance
  - make sure original is backed up safely
      - totally different directory
      - readonly permissions for all users
  - run each processor script
    - write a sentence or two saying why this script now
    - run script and pipe stdout to log file `python do_shit.py previous_step/*/*.rdf > current_step.txt`
    - rename mutated directory `mv previous_step current_step`
    - back up processed dir with `tar -czf current_step.tar.gz current_step`
  - run analysis script