from django.forms import ValidationError
from django.test import TestCase
from users.forms import UserCreateForm, file_size
from django.core.files.uploadedfile import SimpleUploadedFile


class ProfileAddFormTests(TestCase):
    
    def test_profilepic_file_size_limit_function(self):
        
        with self.assertRaises(ValidationError):
            image = SimpleUploadedFile(name='test.jpg',
                                        content=open('media/test_img/test_image.jpg', 'rb').read(),
                                        content_type='image/jpeg')
            file_size(image)
        

      
    def test_usercreateform_password_label(self):
        

        
        form = UserCreateForm()
        self.assertEqual(form['password2'].label, 'Password Confirm')
        