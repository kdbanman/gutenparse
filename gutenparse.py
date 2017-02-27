
import rdflib
import sys

def get_title(g):
  query_string = """
    SELECT ?title WHERE {
      ?book a <http://www.gutenberg.org/2009/pgterms/ebook> .
      ?book dcterms:title ?title
    }
    ORDER BY DESC(?title)
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
    ORDER BY DESC(?year)
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
    ORDER BY DESC(?author)
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
    ORDER BY DESC(?lang)
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
    ORDER BY DESC(?subject)
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
    ORDER BY DESC(?subject)
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

  return [subject.encode('utf-8') for subject in lcsh]

def enumerate_parsed(meta_file_names, callback):
  print "Processing " + str(len(meta_file_names)) + " meta files...\n"

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
