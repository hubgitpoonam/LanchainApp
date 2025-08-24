import os
import requests

from dotenv import load_dotenv
from openai import responses

load_dotenv()


def scrape_linkedin_profile(linkedin_profile_url: str, mock: bool = False):
    """scrape information from LinkedIn profiles,
    Manually scrape information from LinkedIn profiles."""

    if mock:
        # Use different mock data based on the profile URL
        if "poonam-kumari" in linkedin_profile_url.lower():
            mock_url = "https://gist.githubusercontent.com/hubgitpoonam/6940f2117dc0a086bc61f80690ad545c/raw/46a3a82105e20bf7e3bce8c5b6c8b53e863de684/poonam"
        elif "edenmarco" in linkedin_profile_url.lower() or "eden-marco" in linkedin_profile_url.lower():
            mock_url = "https://gist.githubusercontent.com/emarco177/859ec7d786b45d8e3e3f688c6c9139d8/raw/d71c166a85aefb22842570b7aa9a0208008b39ec/mock_data_eden.json"
        else:
            # Default mock data
            mock_url = "https://gist.githubusercontent.com/emarco177/859ec7d786b45d8e3e3f688c6c9139d8/raw/d71c166a85aefb22842570b7aa9a0208008b39ec/mock_data_eden.json"
        
        try:
            response = requests.get(mock_url, timeout=10)
            data = response.json()
            
            # Extract person data from mock response
            if 'person' in data:
                data = data['person']
            
            cleaned_data = {
                'photoUrl': data.get('photoUrl') or data.get('profilePicture'),
                'full_name': f"{data.get('firstName', '')} {data.get('lastName', '')}",
                'headline': data.get('headline', ''),
                'location': data.get('location', ''),
                'about': data.get('about', ''),
                'experiences': data.get('positions', {}).get('positionHistory', []),
                'education': data.get('schools', {}).get('educationHistory', []),
                'skills': data.get('skills', [])
            }
            
            # Remove any None values
            return {k: v for k, v in cleaned_data.items() if v not in (None, "", [], {})}
        except Exception as e:
            print(f"Error loading mock data: {e}")
            return {}
            
    else:
        api_endpoint = "https://api.scrapin.io/enrichment/profile"
        headers = {
            "x-api-key": os.environ["SCRAPIN_API_KEY"]
        }
        params = {
            "linkedInUrl": linkedin_profile_url
        }
        
        try:
            response = requests.get(
                api_endpoint,
                headers=headers,
                params=params,
                timeout=10,
            )
            
            print(params)
            response_data = response.json()
            print("API Response:", response_data)
            
            # Check if we got an error response
            if not response.ok or ('success' in response_data and not response_data['success']):
                print(f"API Error: {response_data}")
                # Fall back to mock data
                return scrape_linkedin_profile(linkedin_profile_url, mock=True)
            
            # Get person data
            data = response_data.get("person", {})
            
            if not data:
                print("No person data found, falling back to mock")
                return scrape_linkedin_profile(linkedin_profile_url, mock=True)
            
            # Format the data consistently
            cleaned_data = {
                'photoUrl': data.get('photoUrl') or data.get('profilePicture'),
                'full_name': f"{data.get('firstName', '')} {data.get('lastName', '')}",
                'headline': data.get('headline', ''),
                'location': data.get('location', ''),
                'about': data.get('about', ''),
                'experiences': data.get('positions', {}).get('positionHistory', []),
                'education': data.get('schools', {}).get('educationHistory', []),
                'skills': data.get('skills', [])
            }
            
            # Remove any None values
            return {k: v for k, v in cleaned_data.items() if v not in (None, "", [], {})}
            
        except Exception as e:
            print(f"Error scraping profile: {e}")
            # Fall back to mock data on error
            return scrape_linkedin_profile(linkedin_profile_url, mock=True)


if __name__ == "__main__":
    print(scrape_linkedin_profile(
        #linkedin_profile_url="https://www.linkedin.com/in/eden-marco/"
        linkedin_profile_url = "https://www.linkedin.com/in/poonam-kumari-430b55229/"
    ))