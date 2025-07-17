from .models import AboutMe, SiteConfiguration


def portfolio_context(request):
    """
    Context processor to add portfolio data to all templates
    """
    context = {}
    
    # Get or create AboutMe instance
    try:
        about_me = AboutMe.objects.first()
        if about_me:
            context['global_about_me'] = about_me
    except AboutMe.DoesNotExist:
        pass
    
    # Get or create SiteConfiguration instance
    try:
        site_config = SiteConfiguration.objects.first()
        if site_config:
            context['site_config'] = site_config
        else:
            # Create default site configuration
            site_config = SiteConfiguration.objects.create()
            context['site_config'] = site_config
    except SiteConfiguration.DoesNotExist:
        pass
    
    # Add current year for footer
    from datetime import datetime
    context['current_year'] = datetime.now().year
    
    return context
