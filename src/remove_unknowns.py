import sys
import os
import shutil
from collections import Counter

import gutenparse

def get_unknowns(meta_dict):
  unknowns = []
  if "UNKNOWN" in meta_dict["title"]:
    unknowns.append("title")
  if len(meta_dict["authors"]) == 0:
    unknowns.append("author")
  if len(meta_dict["languages"]) == 0:
    unknowns.append("language")
  if len(meta_dict["lcc_subjects"]) == 0:
    unknowns.append("lcc")

  return unknowns


if __name__ == "__main__":
  dry_run = False
  if sys.argv[-1] == "--dry":
    dry_run = True
    sys.argv.pop()

  all_unknowns = Counter()
  removed = []

  def remove_if_unknown(meta_dict, meta_file_name):
    unknowns = get_unknowns(meta_dict)
    if len(unknowns) != 0:
      book_directory = os.path.dirname(os.path.realpath(meta_file_name))
      all_unknowns.update(unknowns)

      print "Removing " + book_directory + " for:"
      print unknowns
      print ""

      if not dry_run:
          shutil.rmtree(book_directory)

      removed.append(book_directory)

  gutenparse.enumerate_parsed(sys.argv[1:], remove_if_unknown)

  print "Unknowns encountered during removal:"
  for countee, count in all_unknowns.most_common():
    print countee + " (" + str(count) + ")"

  print "\nRemoved " + str(len(removed)) + " books."
