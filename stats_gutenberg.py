from collections import Counter
import csv
import rdflib
import sys

def get_title(g):
  query_string = """
    SELECT ?title WHERE {
      ?book a <http://www.gutenberg.org/2009/pgterms/ebook> .
      ?book dcterms:title ?title 
    }
  """
  results = g.query(query_string)
  title = "UNKNOWN TITLE"
  for row in results:
    title = row[0].toPython()
  return title.encode('utf-8')

def get_author_birth_year(g):
  query_string = """
    SELECT ?year WHERE {
      ?book a <http://www.gutenberg.org/2009/pgterms/ebook> .
      ?book dcterms:creator ?a .
      ?a <http://www.gutenberg.org/2009/pgterms/birthdate> ?year
    }
  """
  results = g.query(query_string)
  year = "UNKNOWN YEAR"
  for row in results:
    year = int(row[0].toPython())
  return year 

def get_author(g):
  query_string = """
    SELECT ?author WHERE {
      ?book a <http://www.gutenberg.org/2009/pgterms/ebook> .
      ?book dcterms:creator ?a .
      ?a <http://www.gutenberg.org/2009/pgterms/name> ?author
    }
  """
  results = g.query(query_string)
  author = "UNKNOWN AUTHOR"
  for row in results:
    author = row[0].toPython()
  return author.encode('utf-8')

def get_language(g):
  query_string = """
    SELECT ?lang WHERE {
      ?book a <http://www.gutenberg.org/2009/pgterms/ebook> .
      ?book dcterms:language ?l .
      ?l rdf:value ?lang
    }
  """
  results = g.query(query_string)
  language = "UNKNOWN LANGUAGE"
  for row in results:
    language = row[0].toPython()
  return language 

def get_lcc(g):
  query_string = """
    SELECT ?subject WHERE {
      ?book a <http://www.gutenberg.org/2009/pgterms/ebook> .
      ?book dcterms:subject ?s .
      ?s dcam:memberOf dcterms:LCC .
      ?s rdf:value ?subject
    }
  """
  results = g.query(query_string)
  lcc = "UNKNOWN LCC"
  for row in results:
    lcc = row[0].toPython()
  return lcc

def get_lcsh(g):
  query_string = """
    SELECT ?subject WHERE {
      ?book a <http://www.gutenberg.org/2009/pgterms/ebook> .
      ?book dcterms:subject ?s .
      ?s dcam:memberOf dcterms:LCSH .
      ?s rdf:value ?subject
    }
  """
  results = g.query(query_string)
  lcsh = set()
  for row in results:
    subject = row[0].toPython()
    if subject is None:
      continue
    else:
      subject.encode('utf-8')

    if " -- " in subject:
      lcsh.update(subject.split(" -- "))
    else:
      lcsh.add(subject)
  return lcsh

def enumerate_parsed(meta_file_names, callback):
  for meta_file_name in meta_file_names:
    try:
      g = rdflib.Graph()
      g.load(meta_file_name)

      title = get_title(g)
      author = get_author(g)
      author_birth_year = get_author_birth_year(g)
      language = get_language(g)
      lcc = get_lcc(g)
      lcsh = get_lcsh(g)

      meta_dict = {
        "title": title,
        "author": author,
        "author_birth_year": author_birth_year,
        "language": language,
        "lcc": lcc,
        "lcsh_subjects": lcsh
      }

      callback(meta_dict, meta_file_name)
    except UnicodeEncodeError as e:
      sys.stderr.write("UNPROCESSABLE: " + meta_file_name + "\n")
      sys.stderr.write("ENCOUNTERED: " + str(e) + "\n\n")


all_author_birth_decades = Counter()
all_languages = Counter()
all_lcc_general = Counter()
all_lcc = Counter()
all_lcsh = Counter()

csv_file = open('stats.csv', 'w')
csv_writer = csv.writer(csv_file)
csv_writer.writerow(("Title", "Author", "Author Birth Year", "Languuage", "LCC (General)", "LCC (Full)"))

def add_to_stats(meta_dict, meta_file_name):
  print meta_file_name

  title = meta_dict["title"]
  author = meta_dict["author"]
  author_birth_year = meta_dict["author_birth_year"]
  language = meta_dict["language"]
  lcc = meta_dict["lcc"]
  lcsh = meta_dict["lcsh_subjects"]
  lcc_general = lcc
  if "UNKNOWN" not in lcc_general:
    lcc_general = lcc_general[0]

  csv_writer.writerow((title, author, author_birth_year, language, lcc_general, lcc))

  print "TITLE:    " + title
  print "AUTHOR:   (" + str(author_birth_year) + ") " + author
  print "LANG:     " + language
  print "LCC:      " + lcc
  print "----"
  for subject in lcsh:
    print "SUBJECT:  " + subject

  print ""
  print ""

  if type(author_birth_year) == int:
    author_birth_decade = int(author_birth_year / 10) * 10
  else:
    author_birth_decade = author_birth_year

  all_author_birth_decades.update([author_birth_decade])
  all_languages.update([language])
  all_lcc_general.update([lcc_general])
  all_lcc.update([lcc])
  all_lcsh.update(lcsh)


enumerate_parsed(sys.argv[1:], add_to_stats)

csv_file.close()

print "------------------------"
print "------------------------"
print "|| SUMMARY STATISTICS ||"
print "------------------------"
print "------------------------"
print ""

def print_counter(counter):
  for countee, count in counter.most_common():
    if type(countee) == int:
      countee = str(countee)
    elif type(countee) == unicode:
      countee = countee.encode('utf-8')

    print countee + " (" + str(count) + ")"
  
print "ALL AUTHOR BIRTH DECADES:"
print_counter(all_author_birth_decades)

print ""
print "ALL LANGUAGES:"
print_counter(all_languages)

print ""
print "ALL LCC GENERAL SUBJECTS:"
print_counter(all_lcc_general)


print ""
print "ALL LCC SUBJECTS:"
print_counter(all_lcc)

print ""
print "ALL LCSH SUBJECTS:"
print_counter(all_lcsh)
