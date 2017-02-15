import markdown2


def read_sourcefile(filename):
  infile = open(filename, 'r')
  infile_content = infile.read()
  infile.close()
  return infile_content 

# read the metadata key/value pairs that come from the first chunk of the posts file
def parse_metadata(metadata_blob):
  stripped_metadata = metadata_blob.strip()
  metadata_lines = stripped_metadata.split("\n")
  metadata_pairs = []
  for line in metadata_lines:
    pair = line.strip().split(":::")
    stripped_pair = [ s.strip() for s in pair ]
    metadata_pairs.append(stripped_pair)
  return metadata_pairs

# split by post delimiter
# TODO this needs to somehow output the metadata from the top of the source file alongside the list of posts
# { "title": "abc", ... "posts": [the posts] }
def split_source_blob(source_blob):  
  stripped_source_blob = source_blob.strip()
  split_blob = source_blob.split("!!post!!")
  metadata_blob = split_blob[0]
  metadata_pairs = parse_metadata(metadata_blob)
  posts_list = split_blob[1:]
  result_dict = {"metadata":{}}
  for pair in metadata_pairs:
      result_dict["metadata"][pair[0]] = pair[1]
  result_dict['posts'] = posts_list
  return result_dict
  

# strip individual posts of surrounding whitespace
def strip_post_list(post_list):
  stripped_posts = []
  for post in post_list:
    stripped_posts.append(post.strip())
  return stripped_posts

# this should probably return an object with metadata as well, eventually
def convert_md_post_list(md_post_list):
  html_posts = []
  for post in md_post_list:
    post_html = markdown2.markdown(post)
    html_posts.append(post_html)
  return html_posts

# this represents the main functionality of this file.
# uses the posts file to create the object that will be rendered by the jinja2 template
def sourcefile_to_dict(filename="site_source/posts.ssg"):
  source_content = read_sourcefile(filename)
  split_content = split_source_blob(source_content)
  metadata = split_content['metadata']
  stripped_posts = strip_post_list(split_content['posts'])
  html_posts =  convert_md_post_list(stripped_posts)
  return { 
    "metadata": metadata, 
    "posts": html_posts
  }

if __name__ == "__main__":
  print sourcefile_to_dict()
