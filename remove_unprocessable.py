import gutenparse
import sys
import os
import shutil


if __name__ == "__main__":
  all_unprocessable = []
  
  def remove_if_unprocessable(meta_dict, meta_file_name):
    print meta_file_name
    print meta_dict
    if meta_dict is None:
      print "UNPROCESSABLE: " + meta_file_name
      print "ENCOUNTERED: " + str(e)
      print "Removing..." + "\n\n"

      book_directory = os.path.dirname(os.path.realpath(meta_file_name))
      all_unprocessable.append(book_directory)

      #shutil.rmtree(book_directory)
      
  gutenparse.enumerate_parsed(sys.argv[1:], remove_if_unprocessable)

  print "Removed " + str(len(all_unprocessable)) + " unprocessable books."
