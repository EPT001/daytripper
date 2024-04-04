import requests
import json
from django.shortcuts import render
from django.http import HttpResponse
from .forms import TextSearchForm, UserForm,BookmarkForm, ReviewForm
from django.shortcuts import redirect
from django.http import JsonResponse
from .services import text_search, nearby_search, get_place_details
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
import logging
from .models import Bookmark, Review
from django.contrib.auth.decorators import login_required



#signupPage is a page for user the create their account with userForm using the standard django user model 
#if it a post request and form is valid program will save and redirect to loginPage

def signupPage(request):
    form = UserForm()
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            form.save()
            user = form.cleaned_data.get('username')
            messages.success(request, 'Account was created for ' + user)
            return redirect("myapp:loginPage")
    return render(request, 'myapp/signup.html', {'form': form})


#loginPage for user to login into their account if it a post reqeust using django authenticate function to login
#if login success redirect to search page(current_location)

def loginPage(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                return redirect("myapp:current_location")
            else:
                messages.info(request, 'This account is disabled')
                return render(request, 'myapp/login.html')
        else:
            print(f"Invalid login detail: {username},{password}")
            messages.info(request, 'Username or Password is incorrect')
            return render(request, 'myapp/login.html')

    return render(request, 'myapp/login.html')

def logoutUser(request):
    logout(request)
    return redirect('myapp:loginPage')


#search_current_location render template search.html and TextSearchForm taking in query, radius, and type of places 

def search_current_location(request):
    form = TextSearchForm()
    form.fields['query'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Enter current location'})
    form.fields['radius'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Enter radius'})
    form.fields['place_type'].widget.attrs.update({'class': 'form-control'})
    return render(request, 'myapp/search.html', {'form': form})

#This is autocomplete function for textbox help return possible place to put in a list of user combobox 
#using function text_search from services.py

def autocomplete(request):
    term = request.GET.get('term', None)
    if term:
        response = text_search(term)
        if response and 'places' in response:  # Check if response is not empty and contains 'places'
            suggestions = [place.get('formattedAddress') for place in response['places']]
            return JsonResponse(suggestions, safe=False)
    return JsonResponse([], status=200)

#returnplaces is a function that will receive place latitude, longitude, place type that user want to search for 
#and radius around the location using nearby_search function from services.py it will return 20 places of the selected type

def returnplaces(request):
    form = TextSearchForm(request.POST)
    if form.is_valid():
        query = form.cleaned_data['query']
        currentlocation = text_search(query)
        radius = form.cleaned_data['radius']
        place_type = form.cleaned_data['place_type']
        latitude = currentlocation['places'][0]['location']['latitude']
        longitude = currentlocation['places'][0]['location']['longitude']
        # Call the nearby_search function with the form data
        nearby_places = nearby_search(place_type, radius, latitude, longitude)

        # You might need to parse the response and format it appropriately

        # Returning the nearby places as a JSON response
        return JsonResponse(nearby_places)
    else:
        # If form is not valid, return an error message
        return JsonResponse({'error': 'Invalid form data'}, status=400)


def selected_place(request, placeId):
    # Example: Return a response with the placeid
    if placeId:
        return HttpResponse(f'You selected place with ID: {placeId}')
    else:
        return HttpResponse('No placeid provided in the request')


# End Pond code


# jessie code



# Set up logging
logger = logging.getLogger(__name__)


def selected_place(request, placeId):
    if placeId:
        place_details = get_place_details(placeId)
        if place_details.get('status') == 'OK':
            # Extract the latitude and longitude from the place details
            lat = place_details['result']['geometry']['location']['lat']
            lng = place_details['result']['geometry']['location']['lng']
            # Pass them to the context
            description = place_details['result'].get('vicinity')

            if request.method == 'POST':
                if 'bookmark' in request.POST:
                    bookmark_form = BookmarkForm(request.POST)
                    if bookmark_form.is_valid():
                        bookmark = bookmark_form.save(commit=False)
                        bookmark.place_id = placeId
                        bookmark.place_name = place_details['result']['name']  # Save the place name
                        if request.user.is_authenticated:
                            bookmark.user = request.user
                            bookmark.save()
                            messages.success(request, 'Bookmark added successfully!')
                        else:
                            # Use sessions for non-authenticated users
                            session_bookmarks = request.session.get('bookmarks', [])
                            session_bookmarks.append({
                                'place_id': placeId,
                                'place_name': place_details['result']['name']
                            })
                            request.session['bookmarks'] = session_bookmarks
                            messages.success(request, 'Bookmark added to your session successfully!')
                        return JsonResponse({'status': 'success', 'message': 'Bookmark added successfully!'})
                    else:
                        return JsonResponse({'status': 'error', 'message': 'There was an error with your submission.'})

                elif 'review' in request.POST:
                    review_form = ReviewForm(request.POST)
                    if review_form.is_valid():
                        review = review_form.save(commit=False)
                        review.user = request.user
                        review.place_id = placeId
                        review.save()
                        messages.success(request, 'Review added successfully!')
                    else:
                        messages.error(request, 'There was an error with your review submission.')

            # Get existing bookmarks and reviews for the context
            if request.user.is_authenticated:
                bookmarks = Bookmark.objects.filter(place_id=placeId, user=request.user)
            else:
                bookmarks = request.session.get('bookmarks', [])

            reviews = Review.objects.filter(place_id=placeId)

            context = {
                'place_details': place_details['result'],
                'lat': lat,
                'lng': lng,
                'description': description,
                'bookmarks': bookmarks,
                'reviews': reviews,
            }
            return render(request, 'myapp/details.html', context)

        else:
            error_message = place_details.get('error_message', 'No error message provided')
            logger.error(f'Error retrieving place details: {error_message}')
            return HttpResponse('Error retrieving place details')
    else:
        return HttpResponse('No placeid provided in the request')

def user_bookmarks(request):
    user_bookmarks = Bookmark.objects.filter(user=request.user).values('id', 'place_id', 'place_name')
    return render(request, 'myapp/bookmarks.html', {'bookmarks': user_bookmarks})


def delete_bookmark(request, bookmark_id):
    Bookmark.objects.get(id=bookmark_id).delete()
    # Redirect to the bookmarks page with a success message
    return redirect('myapp:user_bookmarks')
