from .models import SiteInfo, Category

def site_settings(request):
    """
    Context processor to make site settings available in all templates
    """
    try:
        site_info = SiteInfo.objects.first()
        categories = Category.objects.all().order_by('name')
        if site_info:
            return {
                'site_info': site_info,
                'site_name': site_info.name,
                'site_company': site_info.company,
                'site_logo': site_info.logo.url if site_info.logo else None,
                'site_contact_email': site_info.contact_email,
                'site_contact_phone': site_info.contact_phone,
                'site_address': site_info.address,
                'site_facebook': site_info.facebook,
                'site_twitter': site_info.twitter,
                'site_instagram': site_info.instagram,
                'site_linkedin': site_info.linkedin,
                'site_youtube': site_info.youtube,
                'site_about_us': site_info.about_us,
                'site_privacy_policy': site_info.privacy_policy,
                'site_terms_conditions': site_info.terms_conditions,
                'site_shipping_policy': site_info.shipping_policy,
                'site_return_policy': site_info.return_policy,
                'site_cancellation_policy': site_info.cancellation_policy,
                'site_refund_policy': site_info.refund_policy,
                'site_total_products': site_info.total_products,
                'site_total_customers': site_info.total_customers,
                'site_total_orders': site_info.total_orders,
                'site_happy_customers': site_info.happy_customers,
                'categories': categories,
            }
        else:
            # Return default values if no site info exists
            return {
                'site_info': None,
                'site_name': 'Sugam Ayurveda',
                'site_company': 'Sugam Ayurveda',
                'site_logo': None,
                'site_contact_email': 'info@sugamayurveda.com',
                'site_contact_phone': '+91 1234567890',
                'site_address': 'Your Address Here',
                'site_facebook': '#',
                'site_twitter': '#',
                'site_instagram': '#',
                'site_linkedin': '#',
                'site_youtube': '#',
                'site_about_us': '',
                'site_privacy_policy': '',
                'site_terms_conditions': '',
                'site_shipping_policy': '',
                'site_return_policy': '',
                'site_cancellation_policy': '',
                'site_refund_policy': '',
                'site_total_products': 0,
                'site_total_customers': 0,
                'site_total_orders': 0,
                'site_happy_customers': 0,
                'categories': categories,
            }
    except:
        # Return default values in case of any error
        return {
            'site_info': None,
            'site_name': 'Sugam Ayurveda',
            'site_company': 'Sugam Ayurveda',
            'site_logo': None,
            'site_contact_email': 'info@sugamayurveda.com',
            'site_contact_phone': '+91 1234567890',
            'site_address': 'Your Address Here',
            'site_facebook': '#',
            'site_twitter': '#',
            'site_instagram': '#',
            'site_linkedin': '#',
            'site_youtube': '#',
            'site_about_us': '',
            'site_privacy_policy': '',
            'site_terms_conditions': '',
            'site_shipping_policy': '',
            'site_return_policy': '',
            'site_cancellation_policy': '',
            'site_refund_policy': '',
            'site_total_products': 0,
            'site_total_customers': 0,
            'site_total_orders': 0,
            'site_happy_customers': 0,
            'categories': Category.objects.all().order_by('name'),
        }
