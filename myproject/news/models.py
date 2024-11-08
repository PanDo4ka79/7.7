from django.db import models
from django.contrib.auth.models import User


class Author(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    rating = models.IntegerField(default=0)

    def update_rating(self):
        # Суммируем рейтинг всех статей автора
        post_ratings = self.post_set.aggregate(postRating=models.Sum('rating'))
        post_sum = post_ratings.get('postRating') or 0

        # Суммируем рейтинг всех комментариев, которые написал сам автор
        comment_ratings = self.user.comment_set.aggregate(commentRating=models.Sum('rating'))
        comment_sum = comment_ratings.get('commentRating') or 0

        # Суммируем рейтинг всех комментариев к статьям автора
        post_comments_ratings = Comment.objects.filter(post__author=self).aggregate(
            commentPostRating=models.Sum('rating'))
        post_comment_sum = post_comments_ratings.get('commentPostRating') or 0

        # Итоговый рейтинг автора
        self.rating = post_sum * 3 + comment_sum + post_comment_sum
        self.save()


class Category(models.Model):
    name = models.CharField(max_length=64, unique=True)



class Post(models.Model):
    author = models.ForeignKey(Author, on_delete=models.CASCADE)

    NEWS = 'NW'
    ARTICLE = 'AR'
    CATEGORY_CHOICES = [
        (NEWS, 'Новость'),
        (ARTICLE, 'Статья'),
    ]

    category_type = models.CharField(max_length=2, choices=CATEGORY_CHOICES, default=ARTICLE)
    created_at = models.DateTimeField(auto_now_add=True)
    category = models.ManyToManyField(Category, through='PostCategory')
    title = models.CharField(max_length=128)
    text = models.TextField()
    rating = models.IntegerField(default=0)

    def get_categories(self):
        return ', '.join([category.category.name for category in self.postcategory_set.all()])

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()

    def preview(self):
        return self.text[:124] + '...'


class PostCategory(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    rating = models.IntegerField(default=0)

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()
