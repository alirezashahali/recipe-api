from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient

from core.models import Ingredient
from recipe.serializers import IngredientSerializer


INGREDIENT_URL = reverse('recipe:ingredient-list')


class PublicIngredientsApiTests(TestCase):
    '''test the publicly available ingredients API'''

    def setUp(self):
        self.client = APIClient()

    def test_login_required(self):
        """test that login is required to access the endpoint"""
        res = self.client.get(INGREDIENT_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

    # def test_login_required(self):
    #     """test that login is required to access the endpoint"""
    #     res = self.client.get(INGREDIENT_URL)

    #     self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

class PrivateIngredientApiTest(TestCase):
    '''test that tests ingredients are available when autharized'''

    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(email = "test@test.com",
                                                        password = "123456")
        self.client.force_authenticate(self.user)

    def test_retrieve_ingredient_list(self):
        """test retrieve a list of ingredients"""

        Ingredient.objects.create(user = self.user, name = 'Kale')
        Ingredient.objects.create(user = self.user, name = 'Salt')

        res = self.client.get(INGREDIENT_URL)

        ingredients = Ingredient.objects.all().order_by('-name')
        serializer = IngredientSerializer(ingredients, many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_ingredients_limited_to_user(self):
        """test that the user ingredient are the only ones awailable"""
        user2 = get_user_model().objects.create_user(email = "bitch@ass.com", password = '123456')
        ingredient = Ingredient.objects.create(user = self.user, name= "tomato")
        Ingredient.objects.create(user = user2, name = "potato")

        res = self.client.get(INGREDIENT_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 1)
        self.assertEqual(res.data[0]['name'], ingredient.name)

    def test_create_ingredient_successful(self):
        """to check if the ingredient is created succesfully"""
        payload = {'name': 'cabbage'}
        res = self.client.post(INGREDIENT_URL,payload)
        exists = Ingredient.objects.filter(user = self.user, name = payload['name']).exists()


        self.assertTrue(exists)


    def test_create_ingredient_unsuccessfull(self):
        """to check if uncompelete request get saved or not"""
        payload = {'name': ""}
        res = self.client.post(INGREDIENT_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)


