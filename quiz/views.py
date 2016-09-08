# -*- coding: utf-8 -*-
from django.shortcuts import render, redirect
from quiz.models import Quiz

def startpage(request):
    context = {
        "quizzes": Quiz.objects.all(),
    }
    return render(request, "quiz/startpage.html", context)

def quiz(request, quiz_number):
    context = {
        "quiz": Quiz.objects.get(quiz_number=quiz_number),
    }
    return render(request, "quiz/quiz.html", context)

def question(request, quiz_number, question_number):
    quiz = Quiz.objects.get(quiz_number=quiz_number)
    questions = quiz.questions.all()
    question = questions[int(question_number) - 1]

    context = {
        "question_number": question_number,
        "question": question.question,
        "answer1": question.answer1,
        "answer2": question.answer2,
        "answer3": question.answer3,
        "quiz": quiz,
    }
    return render(request, "quiz/question.html", context)

def answer(request, quiz_number, question_number):
    saved_answers = request.session.get(quiz_number, {})
    answer = int(request.POST["answer"])
    saved_answers[question_number] = answer
    request.session[quiz_number] = saved_answers

    question_number = int(question_number)
    quiz = Quiz.objects.get(quiz_number=quiz_number)
    num_questions = quiz.questions.count()
    if num_questions == question_number:
        return redirect("completed_page", quiz_number)
    else:
        return redirect("question_page", quiz_number, question_number + 1)

def completed(request, quiz_number):
    quiz = Quiz.objects.get(quiz_number=quiz_number)
    questions = quiz.questions.all()
    saved_answers = request.session[quiz_number]

    num_correct_answers = 0
    for counter, question in enumerate(questions):
        if question.correct == saved_answers[str(counter + 1)]:
            num_correct_answers += 1

    context = {
        "correct": num_correct_answers,
        "total": questions.count(),
    }
    return render(request, "quiz/completed.html", context)
