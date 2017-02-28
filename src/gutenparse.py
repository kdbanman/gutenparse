
import rdflib
import sys

def get_single_result(g, query_string, label):
    """
    query_string must be a single column query
    """
    results = g.query(query_string)
    result = "UNKNOWN " + label.upper()

    if len(results) > 1:
      sys.stderr.write("WARNING: Non-singular " + label + " found.\n")
      sys.stderr.write("         Using only one result.\n")

    for row in results:
      result = row[0].toPython()

    return result

def get_multiple_results(g, query_string, calculate_result_list):
  results = g.query(query_string)
  result_set = set()

  for row in results:
    result = row[0].toPython()
    if result is None:
      continue

    result_set.update(calculate_result_list(result))

  return [result.encode('utf-8') for result in result_set]



def get_title(g):
  query_string = """
    SELECT ?title WHERE {
      ?book a <http://www.gutenberg.org/2009/pgterms/ebook> .
      ?book dcterms:title ?title
    }
    ORDER BY DESC(?title)
  """
  return get_single_result(g, query_string, "title").encode('utf-8')

def get_author_birth_year(g):
  query_string = """
    SELECT ?year WHERE {
      ?book a <http://www.gutenberg.org/2009/pgterms/ebook> .
      ?book dcterms:creator ?a .
      ?a <http://www.gutenberg.org/2009/pgterms/birthdate> ?year
    }
    ORDER BY DESC(?year)
  """
  return get_single_result(g, query_string, "year")

def get_author(g):
  query_string = """
    SELECT ?author WHERE {
      ?book a <http://www.gutenberg.org/2009/pgterms/ebook> .
      ?book dcterms:creator ?a .
      ?a <http://www.gutenberg.org/2009/pgterms/name> ?author
    }
    ORDER BY DESC(?author)
  """
  return get_single_result(g, query_string, "author").encode('utf-8')

def get_language(g):
  query_string = """
    SELECT ?lang WHERE {
      ?book a <http://www.gutenberg.org/2009/pgterms/ebook> .
      ?book dcterms:language ?l .
      ?l rdf:value ?lang
    }
    ORDER BY DESC(?lang)
  """
  return get_single_result(g, query_string, "language")

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

  def calculate_result_list(result):
    return [result[0], result]

  return get_multiple_results(g, query_string, calculate_result_list)

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

  def calculate_result_list(result):
    if " -- " in result:
      return result.split(" -- ")
    else:
      return [result]

  return get_multiple_results(g, query_string, calculate_result_list)

def enumerate_parsed(meta_file_names, callback):
  print "Processing " + str(len(meta_file_names)) + " meta files...\n"

  for meta_file_name in meta_file_names:
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
    "lcc_subjects": lcc,
    "lcsh_subjects": lcsh
    }

    callback(meta_dict, meta_file_name)
