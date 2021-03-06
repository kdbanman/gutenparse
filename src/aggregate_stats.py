
import sys
import unicodecsv as csv
from collections import Counter

import gutenparse

if __name__ == "__main__":
  all_author_birth_years = Counter()
  all_languages = Counter()
  all_lcc = Counter()
  all_lcsh = Counter()

  csv_file = open('stats.csv', 'w')
  csv_writer = csv.writer(csv_file)
  csv_writer.writerow(("ID", "Size (KB)", "Title", "Authors", "Author Birth Years", "Languages", "LCC Subjects"))

  def add_to_stats(meta_dict, meta_file_name):
    print meta_file_name

    title = meta_dict["title"]
    author_names = map(lambda author: author["name"], meta_dict["authors"])
    author_birth_years = map(lambda author: author["birth_year"], meta_dict["authors"])
    languages = meta_dict["languages"]
    lcc = meta_dict["lcc_subjects"]
    lcsh = meta_dict["lcsh_subjects"]
    book_size_kb = meta_dict["book_size_kb"]
    book_id = meta_dict["book_id"]

    csv_writer.writerow((book_id, book_size_kb, title, " -- ".join(author_names), " ".join(map(str, author_birth_years)), ' '.join(languages), ' '.join(lcc)))

    print "TITLE:    " + title
    for author in meta_dict["authors"]:
      print "AUTHOR:   (" + str(author["birth_year"]) + ") " + author["name"]
    print "LANGUAGES:     " + " ".join(languages)
    print "----"
    for subject in lcc:
      print "LCC SUBJECT:      " + subject
    print "----"
    for subject in lcsh:
      print "LCSH SUBJECT:  " + subject

    print ""
    print ""

    all_author_birth_years.update(author_birth_years)
    all_languages.update(languages)
    all_lcc.update(lcc)
    all_lcsh.update(lcsh)


  gutenparse.enumerate_parsed(sys.argv[1:], add_to_stats)

  csv_file.close()

  print "------------------------"
  print "------------------------"
  print "|| SUMMARY STATISTICS ||"
  print "------------------------"
  print "------------------------"
  print ""

  def print_counter(counter):
    for countee, count in counter.most_common():
      if type(countee) == int or type(countee) == long:
        countee = str(countee)
      elif type(countee) == unicode:
        countee = countee.encode('utf-8')

      print str(countee) + " (" + str(count) + ")"

  print ""
  print "ALL LCSH SUBJECTS:"
  print_counter(all_lcsh)

  print ""
  print "ALL LCC SUBJECTS:"
  print_counter(all_lcc)

  print ""
  print "ALL AUTHOR BIRTH YEARS:"
  print_counter(all_author_birth_years)

  print ""
  print "ALL LANGUAGES:"
  print_counter(all_languages)
