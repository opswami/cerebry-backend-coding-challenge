from django.test import TestCase


class CitySearch(TestCase):
    @classmethod
    def setUpTestData(cls):
        '''
                setUpTestData: Run once to set up non-modified data for all class methods
        '''
        print("As we are not using any database for this API so just skipping this setUp")
        pass

    def setUp(self):
        '''
            Setting up testing data every type for each method call
        '''
        self.api_url = '/api/cities/suggestions/'

    def test_city_search_status_code_correct_params(self):
        '''
            Testing APIs response code on a valid request with mandatory params
        '''
        print('Starting : Test city search status code with correct params')
        response = self.client.get(self.api_url + '?q=Lon')
        self.assertEquals(response.status_code, 200)
        print('Completed : Test city search status code with correct params\n')

    def test_city_search_status_code_without_params(self):
        '''
            Testing APIs response code on a valid request without mandatory params
        '''
        print('Starting : Test city search status code with incorrect params')
        response = self.client.get(self.api_url)
        result = self.assertEquals(response.status_code, 404)
        print('Completed : Test city search status code with incorrect params\n')

    def test_api_response_type(self):
        '''
            Testing APIs response type on a valid request without mandatory params
        '''
        print('Starting : Test API response type')
        response = self.client.get(self.api_url + '?q=Lon')
        self.assertEquals(type(response.data), type({}))
        print('Completed : Test API response type\n')
