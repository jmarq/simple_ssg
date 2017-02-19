from parse_posts import sourcefile_to_dict
from subprocess import call
import jinja2

# make sure the output directory doesn't have any "leftovers" in it
def refresh_output_dir():
    rmdir_cmd = ["rm", "-rf", "output"]
    mkdir_cmd = ["mkdir", "output"]
    call(rmdir_cmd)
    call(mkdir_cmd)


# parse posts file and put the content into the template
def render_index():
  template_file = "site_source/index_template.html"
  outfilename = "output/index.html"
  infile = open(template_file,'r')
  template = infile.read()
  infile.close()

  jinja_template = jinja2.Template(template)
  source_dict = sourcefile_to_dict()

  rendered = jinja_template.render(content=source_dict)

  outfile = open(outfilename,'w')
  outfile.write(rendered)
  outfile.close()
  print "rendered %s" % outfilename


# move styles, scripts, and images into output dir
def copy_static():
  static_dirs = ['css', 'js', 'images']
  for directory in static_dirs:
      cmd = ['cp','-r','site_source/%s' % directory, 'output']
      print cmd
      call(cmd)



if __name__ == "__main__":
    refresh_output_dir()
    render_index()
    copy_static()

