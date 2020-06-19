from app.models import Comment, User,Blog
from app import db
import unittest

class BlogTest(unittest.TestCase):
    def setUp(self):
        self.new_user = User(username = 'Minions', password = 'matata', email = 'janedoe@demo.com')
        self.new_blog = Blog(blog_author='Blog', blog_content='Blog content')
        
    def test_check_instance(self):
        
        self.assertEquals(self.new_blog.blog_author,'Blog')
        self.assertEquals(self.new_blog.blog_content, 'Blog content')
        

    def test_save_blog(self):
        self.new_blog.save_blog()
        self.assertTrue(len(Blog.query.all()) > 0)      

    # def tearDown(self):
    #     User.query.delete()
    #     Blog.query.delete()
    #     Comment.query.delete()
    #     db.session.commit()

    def test_get_blog_by_id(self):
        self.new_blog.save_blog()
        blog = Blog.get_blog(1)
        self.assertTrue(blog is not None)