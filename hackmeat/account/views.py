from django.template import RequestContext
from django.shortcuts import render_to_response
from django.contrib import messages
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth import *
from django.template.response import TemplateResponse

import forms 
import models

from django.template.response import TemplateResponse
from django.shortcuts import redirect
from django.conf import settings

import mandrill
import logging

import forms


def processors(request, zipcode=11201):
    return render_to_response('account/processors.html',
                            {
                                'zipcode': zipcode
                            },
                            context_instance=RequestContext(request))


def signup_farmer(request):
    if request.method == 'POST':
        form = forms.FarmerForm(data=request.POST, instance=userprofile)
        if form.is_valid():
            farmer = form.save()
            return redirect('home')
    else:
            form = forms.FarmerForm()
    return TemplateResponse(request, 'account/signup_farmer.html', {
        'form': form

        })


def signup_processor(request):
    if request.method == 'POST':
        uform = forms.UserSignupForm(data=request.POST)
        pform = forms.ProcessorForm(data=request.POST)
        if uform.is_valid() and pform.is_valid():
            user = uform.save()
           
            profile = pform.save(commit = False)
            profile.user = user
            profile.save()
             #Log user in
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(username=username, password=password)
            login(request, user)
            messages.success(request, u'Welcome to the Slot For Slaught')
            return redirect('farmer_dash')
    else:
        uform = forms.UserSignupForm()
        pform = forms.ProcessorForm()
    return TemplateResponse(request, 'account/processor_signup.html', {
        'form': pform,
        'form2': pform,
        })


def settings_farmer(request):
    return render_to_response('account/settings_farmer.html',
                            {},
                            context_instance=RequestContext(request))


def settings_processor(request):
    return render_to_response('account/settings_processor.html',
                            {},
                            context_instance=RequestContext(request))


def processor(request):
    return render_to_response('account/processor.html',
                            {},
                            context_instance=RequestContext(request))


def farmer(request):
    return render_to_response('account/farmer.html',
                            {},
                            context_instance=RequestContext(request))


def user_edit(request):
    user = request.user
    if request.method == 'POST':
        form = forms.UserForm(data=request.POST, instance=user)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = forms.UserForm(instance=user)
    return TemplateResponse(request, 'account/user_edit.html', {
        'form': form,
        'user': user,
        
        })


def login_view(request):
    username = password = ''
    if request.method == 'POST':
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')

        user = authenticate(username=username, password=password)
        if user is not None and user.is_active:
            login(request, user)
            return redirect('farmer_dash')
        else:
            return redirect('farmer_signup')
    return TemplateResponse(request, 'registration/login.html', {
        'username': username,
        'password': password,
 })

def logout_view(request):
    logout(request)
    return TemplateResponse(request, 'registration/logout.html')


def user_signup(request):
    if request.method == 'POST':
        uform = forms.UserSignupForm(data=request.POST)
        
        if uform.is_valid():
            user = uform.save()
             #Log user in
            username = uform.cleaned_data['username']
            password = uform.cleaned_data['password1']
            user = authenticate(username=username, password=password)
            login(request, user)
            messages.success(request, u'Welcome to the Slot For Slaught')
            if uform.cleaned_data['occupation'] == 'FA':
                return redirect('farmer_signup')
    else:
        uform = forms.UserSignupForm()
        pform = forms.UserProfileForm()
    return TemplateResponse(request, 'account/user_signup.html', {
        'form': uform,
        })


def about(request):
    return render_to_response('base/about.html',
                            {},
                            context_instance=RequestContext(request))


def contact(request):
    if request.method == 'POST':
        form = forms.ContactForm(request.POST)
        if form.is_valid():
            try:
                # send the contact information via Mandrill
                m = mandrill.Mandrill(settings.MANDRILL_API_KEY)
                m.messages.send({
                    'text': form.cleaned_data.get('message'),
                    'subject': form.cleaned_data.get('subject'),
                    'name': form.cleaned_data.get('name'),
                    'from_email': form.cleaned_data.get('email'),
                    'to': [{
                        'email': 'gabriel@foodfortherestofus.com',
                        'name': 'Gabriel Key',
                    }],
                })
                logging.info('Sent contact email: {0}'.format(form.cleaned_data))
            except mandrill.InvalidKeyError, e:
                logging.error('Cannot send contact email: {0}'.format(
                    form.cleaned_data))
                logging.exception(e)
            except mandrill.Error, e:
                logging.error('Cannot send contact email: {0}'.format(
                    form.cleaned_data))
                logging.exception(e)
            return redirect('contact_complete')
    else:
        form = forms.ContactForm()

    return TemplateResponse(request, 'base/contact.html', {
        'form': form,
    })
