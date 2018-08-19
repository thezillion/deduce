from .models import Profile
def get_avatar(backend, strategy, details, response,
        user=None, *args, **kwargs):
    url = None
    if backend.name == 'google-oauth2':
        url = response['image'].get('url')
        ext = url.split('.')[-1]
    if url:
        print(user, user.id)
        obj = Profile.objects.get(user_id=user.id)
        obj.profile_picture = url
        obj.save()
