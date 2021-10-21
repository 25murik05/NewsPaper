from django.db import models
from django.contrib.auth.models import User
from django.db.models import Sum


class Author(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    rating = models.IntegerField(default=0)

    def update_rating(self):
        postR = self.post_set.aggregate(postRating=Sum('rating'))
        pRat = 0
        pRat += postR.get('postRating')

        comR = self.user.comment_set.aggregate(commentRating=Sum('rating'))
        cRat = 0
        cRat += comR.get('commentRating')

        self.rating = pRat * 3 + cRat
        self.save()



class Category(models.Model):
    category = models.CharField(max_length=255, unique=True)


class Post(models.Model):
    news = 'N'
    article = 'A'
    NOA = [
        (news, 'Новости'),
        (article, 'Статьи')
    ]
    noa = models.CharField(max_length=1, choices=NOA, default=news)
    time_in = models.DateTimeField(auto_now_add=True)
    heading = models.CharField(max_length=255)
    text = models.TextField()
    rating = models.IntegerField(default=0)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    category = models.ManyToManyField(Category, through='PostCategory')

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        if self.rating != 0:
            self.rating -= 1
            self.save()

    def preview(self):
        return self.text[:124] + '...'


class PostCategory(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)


class Comment(models.Model):
    comment = models.TextField()
    time_in = models.DateTimeField(auto_now_add=True)
    rating = models.IntegerField(default=0)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        if self.rating != 0:
            self.rating -= 1
            self.save()
