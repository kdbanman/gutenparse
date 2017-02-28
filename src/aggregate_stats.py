
import sys
import unicodecsv as csv
from collections import Counter

import gutenparse

if __name__ == "__main__":
  all_author_birth_decades = Counter()
  all_languages = Counter()
  all_lcc = Counter()
  all_lcsh = Counter()

  csv_file = open('stats.csv', 'w')
  csv_writer = csv.writer(csv_file)
  csv_writer.writerow(("Title", "Author", "Author Birth Year", "Language", "LCC Subjects"))

  def add_to_stats(meta_dict, meta_file_name):
    print meta_file_name

    title = meta_dict["title"]
    author = meta_dict["author"]
    author_birth_year = meta_dict["author_birth_year"]
    language = meta_dict["language"]
    lcc = meta_dict["lcc_subjects"]
    lcsh = meta_dict["lcsh_subjects"]

    csv_writer.writerow((title, author, author_birth_year, language, ' '.join(lcc)))

    print "TITLE:    " + title
    print "AUTHOR:   (" + str(author_birth_year) + ") " + author
    print "LANG:     " + language
    print "----"
    for subject in lcc:
      print "LCC SUBJECT:      " + subject
    print "----"
    for subject in lcsh:
      print "LCSH SUBJECT:  " + subject

    print ""
    print ""

    if type(author_birth_year) == int:
      author_birth_decade = int(author_birth_year / 10) * 10
    else:
      author_birth_decade = author_birth_year

    all_author_birth_decades.update([author_birth_decade])
    all_languages.update([language])
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

  print "ALL AUTHOR BIRTH DECADES:"
  print_counter(all_author_birth_decades)

  print ""
  print "ALL LANGUAGES:"
  print_counter(all_languages)
