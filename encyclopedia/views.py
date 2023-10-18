from django.shortcuts import render
from . import util
from markdown2 import Markdown
import random


def markdown_to_html(title):
    """user wirte the content in markdown language. But it must be converted to 
    html before it can be rendered as a webpage when user requested that page. 
    the function takes only "title" parameter and find the related content of the title.
    if there has no content based on the title then the func returns none. If it finds 
    any content which is in markdown language, the func converted the language to the 
    html. """
    content = util.get_entry(title)
    to_markdown = Markdown()
    if content == None:
        return None
    else:
        html_content = to_markdown.convert(content)
        return html_content
    

def index(request):
    """outputs a home page for the app. """
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })


def entry(request, title):
    """when a user cliks a title, a request(/wiki/title) is sent to the server. 
    The current func takes tow parameters: request and title. And return a page 
    containing title and html_content for the users. 
    input: request, title
    output: title, content"""
    html_content = markdown_to_html(title)
    if html_content == None:
        return render(request, "encyclopedia/error_msg.html")
    else:
        return render(request, "encyclopedia/entry.html", {
            "title": title,
            "html_content": html_content
        })
    

def search(request):
    """the func is for searching particular entry in my encyclopedia. 
    In the 'layout.html' file, there is a form tag. In the action atrribute of the form tag
    there is a url by which the form data submitted to the search function of the views.py file
    as a parameter. The method is POST which is used for submitting data to a webpage. 
    let the user searched for 'git'. Then a request sent to the server and the server finds
    the search function to submit the data."""
    if request.method == 'POST':

        to_search = request.POST['q']
        html_content = markdown_to_html(to_search)

        """if there is entry based on the search then the user will see a page 
        containg the searched entry title and html content. Else if there is no precise entry as search but search is a sub-string of any entries
        then the user will see a page contaning all the entries. """

        if html_content is not None:
            return render(request, "encyclopedia/entry.html", {
                'title': to_search,
                'html_content': html_content
            })
          
        else:
            all_entries = util.list_entries()
            mapped_entry = []
            for entry in all_entries:
                if to_search.lower() in entry.lower():
                    mapped_entry.append(entry) 
            entries = render(request, "encyclopedia/mapped.html", {
                "mapped_entry": mapped_entry
            })
            return entries


def create_new_page(request):
    """
    Renders a page for creating a new entry in the encyclopedia.

    If the request method is GET, it displays a form for creating a new entry.
    If the request method is POST, it processes the submitted form data, checks if
    an entry with the same title already exists, and either displays an error message
    or saves the new entry and displays it in HTML format.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponse: A response containing the new entry page or an error message.
    """
    if request.method == "GET":
        return render(request, "encyclopedia/new.html")
    else:
        title = request.POST['title']
        content = request.POST['content']
        is_title_exist = util.get_entry(title)
        if is_title_exist is not None:
            return render(request, "encyclopedia/error_msg.html", {
                "message": "Entry Page Already Exists"
            })
        else:
            util.save_entry(title, content)
            html_content = markdown_to_html(title)
            return render(request, "encyclopedia/entry.html", {
                "title": title,
                "html_content": html_content
            })
        

def edit(request):
    """
    Renders a page for editing an existing entry in the encyclopedia.

    If the request method is POST, it retrieves the content of the entry with the
    specified title and displays it in an editable form.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponse: A response containing the editing form for an entry.
    """
    if request.method == 'POST':
        title = request.POST['title']
        content = util.get_entry(title)
        return render(request, "encyclopedia/edit.html", {
            "title": title,
            "content": content
        })
    
def save_edit(request):
    """
    Saves the edited content of an existing entry in the encyclopedia.

    If the request method is POST, it retrieves the edited content and title,
    updates the entry with the new content, and displays the entry in HTML format.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponse: A response containing the edited entry in HTML format.
    """
    if request.method == 'POST':
        title = request.POST['title']
        content = request.POST['content']
        util.save_entry(title, content)
        html_content = markdown_to_html(title)
        return render(request, "encyclopedia/entry.html", {
            "title": title,
            "html_content": html_content
        })


def random_entry(request):
    """
    Displays a random entry from the encyclopedia.

    It randomly selects an entry from the list of all entries, converts its content
    from Markdown to HTML, and displays it in a page.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponse: A response containing a random entry in HTML format.
    """
    all_entries = util.list_entries()
    rand_entry = random.choice(all_entries)
    html_content = markdown_to_html(rand_entry)
    return render(request, "encyclopedia/entry.html", {
        "title": rand_entry,
        "html_content": html_content
    })
    