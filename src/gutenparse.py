
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

def get_multiple_results(g, query_string, calculate_result_list=None):
  results = g.query(query_string)
  result_set = set()

  for row in results:
    result = row[0].toPython()
    if result is None:
      continue

    if calculate_result_list == None:
      result_set.add(result)
    else:
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

def get_authors(g):
  query_string = """
    SELECT ?author ?year WHERE {
      ?book a <http://www.gutenberg.org/2009/pgterms/ebook> .
      ?book dcterms:creator ?a .
      ?a <http://www.gutenberg.org/2009/pgterms/name> ?author .
      ?a <http://www.gutenberg.org/2009/pgterms/birthdate> ?year
    }
    ORDER BY DESC(?author)
  """
  results = g.query(query_string)

  def author_dict(result_row):
    author_name = result_row[0].toPython()
    author_birth_year = result_row[1].toPython()
    if author_name is None or author_birth_year is None:
      return None

    return {
      "name": author_name.encode('utf-8'),
      "birth_year": author_birth_year
    }

  return [author_dict(row) for row in results if row is not None]

def get_languages(g):
  query_string = """
    SELECT ?lang WHERE {
      ?book a <http://www.gutenberg.org/2009/pgterms/ebook> .
      ?book dcterms:language ?l .
      ?l rdf:value ?lang
    }
    ORDER BY DESC(?lang)
  """
  return get_multiple_results(g, query_string)

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

  return get_multiple_results(g, query_string)

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
    authors = get_authors(g)
    languages = get_languages(g)
    lcc = get_lcc(g)
    lcsh = get_lcsh(g)

    meta_dict = {
    "title": title,
    "authors": authors,
    "languages": languages,
    "lcc_subjects": lcc,
    "lcsh_subjects": lcsh
    }

    callback(meta_dict, meta_file_name)
