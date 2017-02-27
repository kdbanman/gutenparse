import gutenparse
import sys
import os
import shutil


def get_unknowns(meta_dict):
  """
  meta_dict = {
    "title": title,
    "author": author,
    "author_birth_year": author_birth_year,
    "language": language,
    "lcc": lcc,
    "lcsh_subjects": lcsh
  }
  """
  unknowns = []
  if "UNKNOWN" in meta_dict["title"]:
    unknowns.append("title")
  if "UNKNOWN" in meta_dict["author"]:
    unknowns.append("author")
  if "UNKNOWN" in str(meta_dict["author_birth_year"]):
    unknowns.append("author_birth_year")
  if "UNKNOWN" in meta_dict["language"]:
    unknowns.append("language")
  if "UNKNOWN" in meta_dict["lcc"]:
    unknowns.append("lcc")

  return unknowns
  

if __name__ == "__main__":
  all_unknowns = Counter()
  removed = 0
  
  def remove_if_unknown(meta_dict, meta_file_name):
    unknowns = get_unknowns(meta_dict)
    if len(unknowns) != 0:
      book_directory = os.path.dirname(os.path.realpath(meta_file_name))
      all_unknowns.update(unknowns)

      print "Removing " + book_directory + " for:"
      print unknowns
      print ""

      #shutil.rmtree(book_directory)

      removed += 1

  gutenparse.enumerate_parsed(sys.argv[1:], remove_if_unknown, all_unknowns)

  print "Unknowns encountered during removal:"
  for countee, count in counter.most_common():
    print countee + " (" + str(count) + ")"

  print "\nRemoved " + str(removed) + " books."
