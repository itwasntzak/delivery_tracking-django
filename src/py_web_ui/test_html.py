import unittest
import py_web_ui.html as html

class TestClasses(unittest.TestCase):
    def setUp(self):
        self.test_classes = html.Classes()
    
    def test_classes_setter_error(self):
        with self.assertRaises( TypeError ):
            self.test_classes.classes = 42
            self.test_classes.classes = 'testClass'

    def test_add_class(self):
        # when Button.classes is None
        self.test_classes.add_class( 'testClass' )
        self.assertEqual(
            self.test_classes.classes,
            [ 'testClass' ]
        )
        # after Button.classes contains a string
        self.test_classes.add_class( 'anothaOne' )
        self.assertEqual(
            self.test_classes.classes,
            [ 'testClass', 'anothaOne' ]
        )
    
    def test_add_class_errors(self):
        # if passed argument is not a string
        self.assertRaises(
            TypeError,
            self.test_classes.add_class,
            [ 'testClass' ]
        )
        # if Button.classes is not a list
        self.test_classes.classes = { 'myClass': 'testClass' }
        self.assertRaises(
            TypeError,
            self.test_classes.add_class,
            'testClass'
        )


class TestButton(unittest.TestCase):
    def setUp(self):
        self.test_button = html.Button('Next')

    def test_get_attibutes(self):
        self.assertEqual(
            self.test_button.get_attributes(),
            ['type', 'value']
        )
        self.test_button.classes = 'testClass'
        self.assertEqual(
            self.test_button.get_attributes(),
            ['classes', 'type', 'value']
        )
        self.test_button.form = 'testForm'
        self.assertEqual(
            self.test_button.get_attributes(),
            ['classes', 'form', 'type', 'value']
        )

    def test_classes(self):
        # Errors
        # not a list
        with self.assertRaises( TypeError ):
            self.test_button.classes
        # empty list
        self.test_button.classes = []
        self.assertRaises(
            ValueError,
            self.test_button.classes
        )
        # Functionality
        # add first class
        self.test_button.classes = [ 'testClass' ]
        self.assertEqual(
            self.test_button.classes,
            'testClass'
        )
        # add second class
        self.test_button.classes.append( 'myButton' )
        self.assertEqual(
            self.test_button.get_classes,
            'testClass myButton'
        )


    # def test_start_html(self):
    #     self.assertEqual(
    #         self.next_button.html_start(),
    #         '<button type="button"'
    #     )
    #     form_id = 'testForm'
    #     self.next.form = form_id
    #     self.assertEqual(
    #         self.next_button.html_start(
                
    #         ),
    #         f'<button form="{form_id}" type="button"'
    #     )
