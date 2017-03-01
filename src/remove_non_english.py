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

  all_non_english_languages = Counter()
  removed = []

  def remove_if_not_english(meta_dict, meta_file_name):
    languages = [language.upper() for language in meta_dict["languages"]]
    if "EN" not in languages:
      book_directory = os.path.dirname(os.path.realpath(meta_file_name))
      all_non_english_languages.update(languages)

      print "Removing " + ", ".join(languages) + " " + book_directory

      if not dry_run:
          shutil.rmtree(book_directory)

      removed.append(book_directory)

  gutenparse.enumerate_parsed(sys.argv[1:], remove_if_not_english)

  print "\nNon-English languages encountered during removal:"
  for countee, count in all_non_english_languages.most_common():
    print countee + " (" + str(count) + ")"

  print "\nRemoved " + str(len(removed)) + " books."
