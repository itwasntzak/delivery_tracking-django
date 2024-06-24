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
    
    def test_get_classes(self):
        # todo: add more test cases, add tests for errors

        self.test_button.classes = ['testClass']
        self.assertEqual(
            self.test_button.get_classes(),
            'testClass'
        )
        self.test_button.classes.append('myButton')
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
