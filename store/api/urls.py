from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from django.contrib import admin
from django.urls import path,include
from .views import (RegisterView,UserDetailView,menu,topbarmenu,categoriesApi,searchApi,NavbarApi,
courseUserApi,course_info,SendCommentApi,getAllCourses,presell,alluser,getPopularCourses,ContactUsView,
articleInfo,getAllArticles,categorySubCourses,banUserApi,navbarWithSubMenu,deleteUserApi,
getAllComments,categoryViewSet,sendContactAnswer,orderlistApiView,orderRetrieveApiView,ChangePasswordView,
UserAPIView,coursesViewSet,getMainPageInfo,articleViewSet,createPublishArticle,
createDraftArticle,changeUserRole,publishDraftArticle,commentViewSet,offViewset,
UpdateDiscountAPIView,retrieveDraftArticle,menuViewSet,CreateSessionView,
sessionViewSet,getRelatedCourses,contactViewSet,getRelatedSession,
getDetailSessions,discountCodeCheck,registerUser)
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'categories', categoryViewSet)
router.register(r'courses', coursesViewSet)
router.register(r'articles', articleViewSet)
router.register(r'comments', commentViewSet,basename="answerComment")
router.register(r'offs', offViewset,basename="discountCode")
router.register(r'menus', menuViewSet,basename="menus")
router.register(r'sessions', sessionViewSet,basename="changeSessions")
router.register(r'contacts',contactViewSet,basename="contacts")

urlpatterns = [
    path('', include(router.urls)),
    path("token/",TokenObtainPairView.as_view(),name="login"),
    path("token/refresh/",TokenRefreshView.as_view(),name="refreshToken"),
    path("signup/",RegisterView.as_view()),
    path("getme/",UserDetailView.as_view()),
    path("menus/",menu.as_view()),
    path("menus/all/",NavbarApi.as_view(),name="panel_menus"),
    path("menus/topbar/",topbarmenu.as_view()),
    path("category/",categoriesApi.as_view()),
    path('search/<str:query>/', searchApi.as_view(), name='search'),
    path('courseuser/', courseUserApi.as_view(), name='courseUser'),
    path('courseinfo/<str:shortName>/', course_info.as_view(), name='course-info'),
    path('articleinfo/<str:href>/', articleInfo.as_view(), name='article-info'),
    path('category/<str:categoryName>/', categorySubCourses.as_view(), name='categorySubCourses'),
    path('comment/', SendCommentApi.as_view(), name='sendComment'),
    path('allcourses/', getAllCourses.as_view(), name='allcourses'),
    path('allarticles/', getAllArticles.as_view(), name='allarticles'),
    path('allcomment/', getAllComments.as_view(), name='getAllComments'),
    path('courses/presell/', presell.as_view(), name='presell'),
    path('users/', alluser.as_view(), name='allUsers'),
    path('courses/popular/', getPopularCourses.as_view(), name='getPopular'),
    path('contact/', ContactUsView.as_view(), name='contactUs'),
    path('ban/<uuid:id>/', banUserApi.as_view(), name='banUser'),
    path('navbar/', navbarWithSubMenu.as_view(), name='navbar'),
    path('deleteuser/<uuid:pk>/', deleteUserApi.as_view(), name='deleteUser'),
    path('ad/',include(router.urls), name='viewsets'),
    path('contact/answer/',sendContactAnswer.as_view(), name='answerContact'),
    path('order/',orderlistApiView.as_view(), name='getlistOrder'),
    path('order/<int:pk>/',orderRetrieveApiView.as_view(), name='getsingleOrder'),
    path('change_password/', ChangePasswordView.as_view(), name='change_password'),
    path('user/profile/', UserAPIView.as_view(), name='updateProfiles'),
    path('main/', getMainPageInfo.as_view(), name='mainPage'),
    path("article/publish/",createPublishArticle.as_view(),name="publishArticle"),
    path("article/draft/",createDraftArticle.as_view(),name="draftArticle"),
    path("user/role/",changeUserRole.as_view(),name="changeRole"),
    path("article/publishdraft/<str:href>/",publishDraftArticle.as_view(),name="publishDraft"),
    path("off/all/",UpdateDiscountAPIView.as_view(),name="allCoursesDiscount"),
    path('getdraftarticle/<str:href>/', retrieveDraftArticle.as_view(),name="getDraftArticle"),
    path('session/create/<int:course_id>/', CreateSessionView.as_view(),name="createSession"),
    path('relatedcourse/<str:href>/', getRelatedCourses.as_view(),name="getRelatedCourse"),
    #getting all the sessions of a course
    path('relatedsessions/<str:href>/', getRelatedSession.as_view(),name="getRelatedSession"),
    path('session/detail/<str:href>/<int:pk>/', getDetailSessions.as_view(),name="getRelatedSession"),
    path('off/<str:code>/', discountCodeCheck.as_view(),name="checkDiscountCode"),
    path('register/<str:href>/', registerUser.as_view(),name="registerUserToCourse"),
]