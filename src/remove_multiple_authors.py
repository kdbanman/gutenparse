import sys
import os
import shutil
from collections import Counter

import gutenparse


if __name__ == "__main__":
  dry_run = False
  if sys.argv[-1] == "--dry":
    dry_run = True
    sys.argv.pop()

  all_removed_authors = Counter()
  removed = []

  def remove_if_multiple_authors(meta_dict, meta_file_name):
    authors = meta_dict["authors"]
    if len(authors) > 1:
      book_directory = os.path.dirname(os.path.realpath(meta_file_name))
      author_names = [author["name"] for author in authors]
      all_removed_authors.update(author_names)

      print "Removing " + book_directory + " for authors " + " -- ".join(author_names)

      if not dry_run:
          shutil.rmtree(book_directory)

      removed.append(book_directory)

  gutenparse.enumerate_parsed(sys.argv[1:], remove_if_multiple_authors)

  print "\nCollaborating authors encountered during removal:"
  for countee, count in all_removed_authors.most_common():
    print countee + " (" + str(count) + ")"

  print "\nRemoved " + str(len(removed)) + " books."
