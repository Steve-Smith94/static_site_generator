import unittest
from htmlnode import HTMLNode 

# Create a test function (usually starts with "test_")
def test_props_to_html_no_props():
    # 1. Create an HTMLNode object
    node = HTMLNode()  # This has props=None by default
    
    # 2. Call the method you want to test
    result = node.props_to_html()
    
    # 3. Check if the result is what you expected
    expected = ""
    if result == expected:
        print("Test passed!")
    else:
        print(f"Test failed! Expected '{expected}', but got '{result}'")


def test_props_to_html_one_prop():
    # Create an HTMLNode with one prop
    node = HTMLNode(props={"href": "https://www.google.com"})
    
    # Call the method
    result = node.props_to_html()
    
    # Check the result
    expected = " href=\"https://www.google.com\""
    if result == expected:
        print("Test with one prop passed!")
    else:
        print(f"Test failed! Expected '{expected}', but got '{result}'")


def test_props_to_html_multiple_props():
    # Create an HTMLNode with multiple props
    node = HTMLNode(props={"href": "https://www.google.com", "target": "_blank"})
    
    # Call the method
    result = node.props_to_html()
    
    # Check the result - should have both attributes
    expected = " href=\"https://www.google.com\" target=\"_blank\""
    if result == expected:
        print("Test with multiple props passed!")
    else:
        print(f"Test failed! Expected '{expected}', but got '{result}'")


test_props_to_html_multiple_props()
test_props_to_html_one_prop()
test_props_to_html_no_props()
    