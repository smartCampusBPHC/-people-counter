import os
import webapp2
import jinja2



template_dir = os.path.join(os.path.dirname(__file__),'template')
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir),autoescape = True)
tokens=list()

class Handler(webapp2.RequestHandler):
    def write(self,*a,**kw):
        self.response.out.write(*a, **kw)

    def render_str(self, template, **params):
        t = jinja_env.get_template(template)
        return t.render(params)

    def render(self, template, **kw):
        self.write(self.render_str(template, **kw))

class People_Count(Handler):

	def get(self):	
		
		#open file
		#read file and store the number in the variable "people_count"
		#close file

		self.render('info.html',params=people_count)           
		
app=webapp2.WSGIApplication([('/people_count', People_Count)], debug=True)
	
