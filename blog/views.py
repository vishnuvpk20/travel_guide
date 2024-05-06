from django.shortcuts import render
from .models import Post
import pandas as pd
from django.http import HttpResponse
import os
from django.views.decorators.csrf import ensure_csrf_cookie
from django.views.decorators.csrf import csrf_protect, csrf_exempt
import json


def home(request):
    context = {
        'posts': Post.objects.all()
    }
    return render(request, 'blog/home.html', context)


def about(request):
    return render(request, 'blog/about.html', {'title': 'About'})

def landing_page(request):
    return render(request, 'blog/landing_page.html')

@csrf_protect
def data_table(request):
    df_country_details = pd.read_csv("country_etiquette_data.csv")
    df_country_details = df_country_details.drop_duplicates(subset='Detail')
    df_country_details['Detail'] = df_country_details['Detail'].str.replace('\r\n', '')
    if request.method == 'POST':
        selected_country = request.POST.get('country')
        # The `country_data` variable is filtering the DataFrame `df_country_details` based on the
        # selected country received from the POST request. It selects rows from `df_country_details`
        # where the 'Country' column matches the selected country.
        country_data = df_country_details[df_country_details['Country'] == selected_country]
        grouped = country_data.groupby(['Country', 'Section'])['Detail'].apply(list).reset_index()
        country_json = grouped.to_json(orient ='records')
        country_json = json.loads(country_json)
        countries = df_country_details['Country'].unique()

        general_detail = list(country_data[country_data.Section =="The People"]["Detail"])[0]
        return render(request, 'blog/country_details.html', {'country_data': country_json, 'countries': countries,'selected_country':selected_country,'general_detail':general_detail})
    else:
        countries = df_country_details['Country'].unique()
        return render(request, 'blog/country_details.html', {'countries': countries})
    # return render(request, 'blog/country_details.html')
