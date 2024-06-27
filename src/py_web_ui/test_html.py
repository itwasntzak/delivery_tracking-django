import unittest
import py_web_ui.html as html

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


    def test_add_class(self):
        # Errors
        # if passed argument is not a string
        self.assertRaises(
            TypeError,
            self.test_button.add_class,
            [ 'testClass' ]
        )
        # if Button.classes is not a list
        self.test_button.classes = { 'myClass': 'testClass' }
        self.assertRaises(
            TypeError,
            self.test_button.add_class,
            'testClass'
        )
        # Functionality
        # when Button.classes is None
        self.test_button.classes = None
        self.test_button.add_class( 'testClass' )
        self.assertEqual(
            self.test_button.classes,
            [ 'testClass' ]
        )
        # after Button.classes contains a string
        self.test_button.add_class( 'anothaOne' )
        self.assertEqual(
            self.test_button.classes,
            [ 'testClass', 'anothaOne' ]
        )


    def test_get_classes(self):
        # Errors
        # if Button.classes is not a list
        self.assertRaises(
            TypeError,
            self.test_button.get_classes
        )
        # if list is empty
        self.test_button.classes = []
        self.assertRaises(
            ValueError,
            self.test_button.get_classes
        )
        # Functionality
        # add first class
        self.test_button.classes.append( 'testClass' )
        self.assertEqual(
            self.test_button.get_classes(),
            'testClass'
        )
        # add second class
        self.test_button.classes.append( 'myButton' )
        self.assertEqual(
            self.test_button.get_classes(),
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
