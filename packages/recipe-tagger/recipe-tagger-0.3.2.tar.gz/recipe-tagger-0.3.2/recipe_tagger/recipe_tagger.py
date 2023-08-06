import io
import numpy as np
import pkgutil
import re
import wikipediaapi

from .foodcategory import FoodCategory
from collections import Counter
from PyDictionary import PyDictionary
from pyfood.utils import Shelf
from textblob import Word

embedding_path = 'data/ingredient_embedding.npy'

def lemmatize_word(word):
    """
    Lemmatize the provided word.
    Lemmatization is the process of converting a word to its base form. 

    :param word: the word to be lemmatized.
    :return: the word lemmatized. 
    """
    w = Word(word)
    return w.lemmatize()

def is_ingredient_vegan(ingredient): 
    """
    Check if the provided ingredient is vegan or not.

    :param ingredient: the name of the ingredient.
    :return: a bool indicating whether the ingredient is vegan or not.
    """
    shelf = Shelf('Milan', month_id=0)
    results = shelf.process_ingredients([ingredient])
    return results['labels']['vegan']

def is_recipe_vegan(ingredients):
    """
    Check if the provided ingredients contained in a recipe ar vegan or not.
    If only one element is not vegan the recipe is not vegan.

    :param ingredients: the list of the ingredients.
    :return: a bool indicating wheter the recipe is vegan or not. 
    """
    shelf = Shelf('Milan', month_id=0)
    results=shelf.process_ingredients(ingredients)
    return results['labels']['vegan']

def search_ingredient_class(ingredient):
    """
    Search on wikipedia and english dictionary the class of the provided ingredient.
    Returns the most occurrences of a single FoodCategory class based on the two research. 

    :param ingredient: the name of the ingredient.
    :return: the class of the ingredient.
    """
    dictionary = PyDictionary()
    wiki = wikipediaapi.Wikipedia('en')

    page = wiki.page(ingredient)
    ontology = ', '.join(dictionary.meaning(ingredient)['Noun'])
    
    categories = []
    for category in FoodCategory:
        if page and re.search(r'\b({0})\b'.format(category.name), page.summary):
            categories.append(category.name)
        if re.search(r'\b({0})\b'.format(category.name), ontology):
            categories.append(category.name)
    if categories:
        return max(categories,key=categories.count) 
    else:
        return categories

def get_ingredient_class(ingredient):
    """
    Predict the class of the provided ingredient based on the embeddings. 
    If the ingredient cannot be found in the dictionary it will be searched on wikipedia pages.

    :param ingredient: the name of the ingredient.
    :return: the class of the ingredient.
    """
    embedding = io.BytesIO(pkgutil.get_data(__name__, embedding_path))
    embedding = np.load(embedding, allow_pickle=True).item()
    if ingredient in embedding:
        lemmatized_ing = lemmatize_word(ingredient)
        return FoodCategory(embedding[lemmatized_ing]).name
    else:
        return search_ingredient_class(ingredient)

def get_recipe_class_percentage(ingredients):
    """
    Classify a recipe in tags based on its ingredient. 
    Returns the percentages of ingredient class in the recipe provided.

    :param ingredients: list of ingredients in the recipe.
    :return: list of tuples containg classes and percentages. 
    """
    tags = [get_ingredient_class(ingredient) for ingredient in ingredients]  
    c = Counter(tags)
    return [(i, str(round(c[i] / len(tags) * 100.0, 2)) + '%') for i in c]

def get_recipe_tags(ingredients):
    """
    Classify a recipe in tags based on its ingredient. 
    Tag could be: Vegetable, Fruit, Meat, Legume, Diary, Egg. 

    :param ingredients: list of ingredients in the recipe.
    :return: set of tags for the recipe. 
    """
    return list(set([get_ingredient_class(ingredient) for ingredient in ingredients]))               