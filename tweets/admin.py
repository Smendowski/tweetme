from django.contrib import admin

# Register your models here.
from .models import Tweet, TweetLike

class TweetLikeAdmin(admin.TabularInline):
  model = TweetLike


class TweetAdmin(admin.ModelAdmin):
  inlines = [TweetLikeAdmin]
  # każdy tweet niech bęzie wświetlony z id usera czyli user, zgodnie z metodą __str__ która jest w models.py. Sposób wyświetlania tweeta w django admin. domyslnie __str__ wyświetla cały obiekt Tweet. Jeśli nadpiszemy __str__ jako return self.content bedziemy w kolumanch mieli tylko content.
  list_display = ['__str__', 'user']
  # Django admin, dostaję search Boxa :)
  search_fields = ['user__username', 'user__email']
  class Meta:
    model = Tweet



admin.site.register(Tweet, TweetAdmin)