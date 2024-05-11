from django.shortcuts import render
from .models import Post
import pandas as pd
from django.http import HttpResponse
import os
from django.views.decorators.csrf import ensure_csrf_cookie
from django.views.decorators.csrf import csrf_protect, csrf_exempt
import json

from django.shortcuts import render
from django.http import HttpResponse
from transformers import GPT2Tokenizer, GPT2LMHeadModel

# Load the pre-trained language model and tokenizer
def load_lm_model(model_dir):
    model = GPT2LMHeadModel.from_pretrained(model_dir)
    tokenizer = GPT2Tokenizer.from_pretrained(model_dir)
    return model, tokenizer

# Function to generate response using the language model
def generate_response(model, tokenizer, prompt, max_length=75):
    input_ids = tokenizer.encode(prompt, return_tensors="pt")
    output_ids = model.generate(input_ids, max_length=max_length, num_return_sequences=1)
    response = tokenizer.decode(output_ids[0], skip_special_tokens=True)
    return response

# Initialize the model and tokenizer
model, tokenizer = load_lm_model(model_dir="travel_guide/lm_model")

def chatbot(request):
    if request.method == 'POST':
        user_input = request.POST.get('user_input', '')
        if user_input:
            # Generate response using the language model
            response = generate_response(model, tokenizer, user_input)
            return render(request, 'blog/chatbot.html', {'user_input': user_input, 'response': response})

    return render(request, 'blog/chatbot.html', {'user_input': '', 'response': ''})



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
