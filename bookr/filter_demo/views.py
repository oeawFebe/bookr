from django.shortcuts import render

def index(request):
    names='jon,doe,mark,swain'
    return render(request,"index.html",{'names':names})
def greeting_view(request):
    books={
        "The night rider":"Ben Author",
        "The Justice":"Don Ameban"
    }
    return render(request,'simple_tag_template.html',{'username':'jdoe',"books":books})
