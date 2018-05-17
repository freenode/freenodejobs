SITE_URL = 'https://{{ canonical_domain_name }}'
SECRET_KEY = '{{ secret_key }}'
KEYERROR_SECRET_KEY = '{{ keyerror_secret_key }}'

ANYMAIL = {
    'AMAZON_SES_CLIENT_PARAMS': {
        'region_name': '{{ aws_ses_region }}',
    },
}
