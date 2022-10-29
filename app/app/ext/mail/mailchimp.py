from mailchimp import Mailchimp

api_key = '25e54006ddf405e47c6110daadecd857-us10'
campaign_id = '1882913'

mailchimp = Mailchimp(api_key)

def send_email_welcome(name,email):
    try:
        res = mailchimp.campaigns.send(campaign_id)
    except Exception as e:
        print(e)
        return str(e)
    return res