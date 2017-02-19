from parse_posts import sourcefile_to_dict
from subprocess import call
import jinja2


class SiteBuilder(object):
    def __init__(self, source_dir="site_source",template_file="index_template.html", output_dir="output", outfile_name="index.html", posts_source="posts.ssg", static_dirs=['js','css','images']):
        self.source_dir = source_dir
        self.template_file = source_dir+"/"+template_file
        self.posts_source = source_dir+"/"+posts_source
        self.output_dir = output_dir
        self.outfile_name = output_dir+"/"+outfile_name
        self.static_dirs = static_dirs

# make sure the output directory doesn't have any "leftovers" in it
    def refresh_output(self):
        rmdir_cmd = ["rm", "-rf", self.output_dir]
        mkdir_cmd = ["mkdir", self.output_dir]
        call(rmdir_cmd)
        call(mkdir_cmd)

# move styles, scripts, and images into output dir
    def copy_static(self):
        for directory in self.static_dirs:
            cmd = ['cp','-r', self.source_dir+'/%s' % directory, self.output_dir]
            print cmd
            call(cmd)

# parse posts file into something that can be rendered into a template
    def posts_to_dict(self):
        return sourcefile_to_dict(self.posts_source)

    def render_template(self, template_string, source_dict):
        jinja_template = jinja2.Template(template_string)
        rendered_html_string = jinja_template.render(content=source_dict)
        return rendered_html_string

# parse posts file and put the content into the template
    def render_index(self):
        infile = open(self.template_file,'r')
        template_string = infile.read()
        infile.close()

        source_dict = self.posts_to_dict()
        rendered_html_string = self.render_template(template_string, source_dict)
        outfile = open(self.outfile_name,'w')
        outfile.write(rendered_html_string)
        outfile.close()
        print "rendered %s" % self.outfile_name

# this is the main method to be used to build the site
    def build(self):
        self.refresh_output()
        self.copy_static()
        self.render_index()


if __name__ == "__main__":
    builder = SiteBuilder()
    builder.build()

