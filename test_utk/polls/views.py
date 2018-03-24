#from django.shortcuts import render

# Create your views here.
from django.http import HttpResponseRedirect, HttpResponse, Http404
from django.template import loader
from django.shortcuts import get_object_or_404, render
from django.urls import reverse

from . import models
"""
def index(request):
    latest_question_list = models.Question.objects.all()
    response = "Hello, world. You're at the polls index"#.<br>"
    #response += ', '.join([q.question_text for q in latest_question_list])

    #using template
    template = loader.get_template('polls/index.html')
    context = {
        'header': response,
        'latest_question_list': latest_question_list,
    }
    #return HttpResponse(response)
    #return HttpResponse(template.render(context, request))
    
    #shortcut render(request, template name, context)
    return render(request, 'polls/index.html', context)
"""

def index(request):
    latest_question_list = models.Question.objects.all()
    response = "Hello, world. You're at the polls index"#.<br>"

    #using template
    #template = loader.get_template('polls/index.html')
    context = {
        'header': response,
        'latest_question_list': latest_question_list
    }
    
    #shortcut render(request, template name, context)
    return render(request, 'polls/index.html', context)

"""
def detail(request, question_id):
    try:
        question = models.Question.objects.get(pk=question_id)
    except models.Question.DoesNotExist:
        raise Http404("Question does not exist")

    response = "You're looking at question %s."
    return HttpResponse(response%question)
"""

def detail(request, question_id):
    question = get_object_or_404(models.Question, pk=question_id)
    return render(request, 'polls/details.html', {'question':question})
"""
def results(request, question_id):
    response = "You're looking at the results of question %s."
    return HttpResponse(response%question_id)
"""
def results(request, question_id):
    question = get_object_or_404(models.Question, pk=question_id)
    return render(request, 'polls/results.html', {'question':question})

"""
def vote(request, question_id):
    response = "You're voting on question %s."
    return HttpResponse(response%question_id)
"""

def vote(request, question_id):
    question = get_object_or_404(models.Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
        selected_choice.votes += 1
        selected_choice.save()
        
        return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))
    
    except (KeyError, models.Choice.DoesNotExist):
        return render(request, 'polls/details.html',
        {
            'question':question,
            'error_message': "You didn't seleceted any choice, you moron!",
        })
