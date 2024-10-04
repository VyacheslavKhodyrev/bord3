from django.conf.urls.static import static
from django.urls import path

from django.conf import settings
from .views import *


urlpatterns = [
   path('', PostsList.as_view(), name='posts'),
   path('<int:pk>/', PostDetail.as_view(), name='post'),
   path('create/', PostCreate.as_view(), name='post_create'),
   path('<int:pk>/update/', PostUpdate.as_view(), name='post_update'),
   path('<int:pk>/delete/', PostDelete.as_view(), name='post_delete'),
   path('<int:pk>/comment/', CommentCreate.as_view(), name='comment_create'),
   path('<int:pk>/comment/delete/', CommentDelete.as_view(), name='comment_delete'),
   path('comments/', CommentsList.as_view(), name='comments'),
   path('category/<int:pk>', CategoryListView.as_view(), name='category_list'),
   path('comment/<int:pk>/status/', comment_status, name='comment_status'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)













