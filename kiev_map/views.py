import random
import ast

from django.shortcuts import render, render_to_response
from django.template import RequestContext

from .models import *

import json


def custom_404(request):
    response = render_to_response('404.html', {},
                                  context_instance=RequestContext(request))
    response.status_code = 404
    return response


def custom_500(request):
    response = render_to_response('500.html', {},
                                  context_instance=RequestContext(request))
    response.status_code = 500
    return response


def add_dists():
    filename_start = "data/district"
    filename_end = ".txt"
    for i in range(10):
        filename = filename_start + str(i) + filename_end
        f = open(filename, "r", encoding="utf8")
        dist_name = f.readline()
        dist_info = f.read()
        print(dist_name)
        if i == 1:
            print(dist_info)
        f.close()
        p = District(name=dist_name,info=dist_info)
        p.save()


def add_street(st, end):
    filename_start = "data/street"
    filename_end = ".txt"
    for i in range(st,end):
        filename = filename_start + str(i) + filename_end
        f = open(filename, "r", encoding="utf8")
        street_name = f.readline()
        street_asm = f.readline()
        st_districts = f.readline().split(',')
        links = f.readline().split(",")
        st_info = f.read()
        street_short = st_info[:100]

        p = Street(name=street_name, info=st_info, ism_id=street_asm, shortIntro=street_short)
        p.save()

        f.close()
        photos = []
        i = 0
        for link in links:

            photo = Photos(caption=street_name+str(i),info=street_name,file = link)
            photo.save()
            photos.append(photo)
            i += 1
        for d in st_districts:
            dist = District.objects.filter(name__exact=d).first()
            p.districts.add(dist)
            for photo in photos:
                photo.districts.add(dist)
                photo.streets.add(p)
                photo.save()
            p.save()


def create_database():

    return


def district_id(request, pk_district):
    #add_street(38,39)

    district = District.objects.filter(id=pk_district).first()
    photos = Photos.objects.filter(districts__name=district.name).order_by('?').all()
    text = district.info.split('\n')
    photos_num = len(photos)
    text_num = len(text)
    range_min = min(text_num,photos_num)
    range_max = max(text_num,photos_num)

    avg = int(range_max/range_min)
    text_pairs = []
    text_iter = 0
    if text_num > photos_num:
        for i in range(range_min-1):
            text_for_pair = ''
            for j in range(avg):
                text_for_pair += (text[text_iter]+"\n")
                text_iter += 1
            text_pairs.append([photos[i],text_for_pair])
        if range_max == text_num:
            text_for_pair = ''
            while text_iter < range_max:
                text_for_pair += (text[text_iter])
                text_iter += 1
            text_pairs.append([photos[range_min - 1],text_for_pair])
    else:
        for i in range(text_num - 1):
            text_pairs.append([photos[i],text[i]])

    streets = Street.objects.filter(districts__name=district.name).order_by('?')[:min(3,Street.objects.filter(districts__name=district.name).count())]

    photos_streets = {}
    for street in streets:
        photo = Photos.objects.filter(streets__name=street.name).order_by('?').first()
        if photo is not None:
            photos_streets[street] = photo.file

    context = {
        'district': district,
        'text_pairs': text_pairs,
        'streets': streets,
        'photos_streets':photos_streets,
    }

    return render(request, 'kiev_map/district.html', context)


def street_id(request,pk_street):
    street = Street.objects.filter(id=pk_street).first()

    photos = Photos.objects.filter(streets__name=street.name).all()
    text = street.info.split('\n')
    photos_num = len(photos)
    text_num = len(text)
    range_min = (min(text_num, photos_num))
    range_max = max(text_num, photos_num)
    link = ""
    words = street.ism_id.split(" ")
    words.append("Київ")
    for word in words:
        link += word
        link += "+"
    link = link[:-1]
    avg = int(range_max / range_min)
    text_pairs = []
    text_iter = 0
    for i in range(range_min):
        text_for_pair = ''
        for j in range(avg):
            text_for_pair += (text[text_iter])
            text_iter += 1
        text_pairs.append([photos[i], text_for_pair])
    if range_max == text_num:
        text_for_pair = ''
        while text_iter < range_max:
            text_for_pair += (text[text_iter])
            text_iter += 1
        if len(text_for_pair) > 0:
            text_pairs.append([photos[range_min-1], text_for_pair])
    context = {
        'street': street,
        'text_pairs': text_pairs,
        'link': link
    }
    return render(request, 'kiev_map/street.html', context)

    #return render(request, 'kiev_map/district.html', context)


def streets(request):
    all_streets = Street.objects.order_by('?').all()
    photos = {}

    for street in all_streets:

            photo = Photos.objects.filter(streets__name=street.name).order_by('?').first()
            if photo is not None:
                photos[street] = photo.file
    return render(request, 'kiev_map/allStreets.html', {'all_streets': all_streets, 'photos': photos})


def districts(request):

    all_districts = District.objects.order_by('?').all()
    photos = {}

    for dist in all_districts:
        photo = Photos.objects.filter(districts__name=dist.name).order_by('?').first()
        if photo is not None:
             photos[dist] = photo.file

    return render(request, 'kiev_map/allDistricts.html', {'all_districts': all_districts, 'photos': photos})


def streets_by_district(request, pk_district):
    district = District.objects.get(id = pk_district)
    streets = Street.objects.filter(districts__name=district.name).order_by('?').all()

    photos = {}

    for street in streets:

        photo = Photos.objects.filter(streets__name=street.name).order_by('?').first()
        if photo is not None:
            photos[street] = photo.file
    return render(request, 'kiev_map/streetsByDistrict.html',
                  {'all_streets': streets, 'photos': photos, 'district': district})


def main_page(request):

    all_districts = District.objects.order_by('?').all()[:4]
    photos = {}
    all_streets = Street.objects.order_by('?').all()[:4]
    for dist in all_districts:
        photo = Photos.objects.filter(districts__name=dist.name).order_by('?').first()
        if photo is not None:
             photos[dist] = photo.file

    for street in all_streets:
        photo = Photos.objects.filter(streets__name=street.name).order_by('?').first()
        if photo is not None:
            photos[street] = photo.file

    return render(request, 'kiev_map/mainPage.html',
                  {'all_districts': all_districts, 'photos': photos, 'all_streets': all_streets})


def create_questions():
    filename = "data/questions.txt"
    f = open(filename, "r", encoding="utf8")
    for i in range(22):
        question = f.readline()
        num = int(f.readline())
        ans = {}
        for j in range(num):
            line = f.readline()
            letter = line.split(' ')
            ans[letter[0]] = line[1:]
        correct_ans = f.readline()[:-1]
        question_ = Question(question=question, answers=ans, correct_answer=correct_ans)
        question_.save()

    f.close()


def quiz(request):
    questions = []
    questions_ = Question.objects.order_by('?').all()
    for q in questions_:
        question = []
        question.append(q.question)
        answers = ast.literal_eval(q.answers)
        question.append(answers)
        question.append(q.correct_answer)
        questions.append(question)

    return render(request, 'kiev_map/quiz.html', context={'questions': questions} )

