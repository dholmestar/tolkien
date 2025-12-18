from htmlnode import HTMLNode, LeafNode, ParentNode #type: ignore


def test_props_to_html_none():
    node = HTMLNode("a", "link", props=None)
    assert node.props_to_html() == ""

def test_props_to_html_empty():
    node = HTMLNode("a", "link", props={})
    assert node.props_to_html() == ""

def test_props_to_html_multiple():
    props = {
        "href": "https://www.google.com",
        "target": "_blank",
    }
    node = HTMLNode("a", "link", props=props)
    assert node.props_to_html() == ' href="https://www.google.com" target="_blank"'

def test_leaf_to_html_p():
    node = LeafNode("p", "Hello, world!")
    assert node.to_html() == "<p>Hello, world!</p>"

def test_leaf_no_tag_returns_value():
    node = LeafNode(None, "Just text")
    assert node.to_html() == "Just text"

def test_to_html_with_children(self):
    child_node = LeafNode("span", "child")
    parent_node = ParentNode("div", [child_node])
    self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

def test_to_html_with_grandchildren(self):
    grandchild_node = LeafNode("b", "grandchild")
    child_node = ParentNode("span", [grandchild_node])
    parent_node = ParentNode("div", [child_node])
    self.assertEqual(
        parent_node.to_html(),
        "<div><span><b>grandchild</b></span></div>",
    )

def test_to_html_with_multiple_children(self):
    child1 = LeafNode("b", "Bold")
    child2 = LeafNode(None, " normal")
    parent = ParentNode("p", [child1, child2])
    self.assertEqual(parent.to_html(), "<p><b>Bold</b> normal</p>")

def test_to_html_with_props(self):
    child = LeafNode(None, "hello")
    parent = ParentNode("div", [child], {"class": "greeting"})
    self.assertEqual(parent.to_html(), '<div class="greeting">hello</div>')

def test_to_html_raises_without_tag(self):
    child = LeafNode(None, "hi")
    parent = ParentNode(None, [child])
    with self.assertRaises(ValueError):
        parent.to_html()

def test_to_html_raises_without_children(self):
    parent = ParentNode("div", None)
    with self.assertRaises(ValueError):
        parent.to_html()