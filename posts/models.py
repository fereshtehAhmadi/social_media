from django.db import models
from accounts.models import User


class Posts(models.Model):
    content = models.TextField()
    views = models.IntegerField()
    create = models.DateTimeField(auto_now_add=True)
    update = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.user.user.username
    

class Gallery(models.Model):
    image = models.ImageField(upload_to='posts/')
    post = models.ForeignKey(Posts, on_delete=models.CASCADE)


class LikePost(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Posts, on_delete=models.CASCADE)
    like = models.BooleanField(default=True)


class Comment(models.Model):
    content = models.TextField()
    create = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Posts, on_delete=models.CASCADE)


class LikeComment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE)
    like = models.BooleanField(default=True)


class ReplyComment(models.Model):
    content = models.TextField()
    create = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE)


class LikeReply(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    reply = models.ForeignKey(ReplyComment, on_delete=models.CASCADE)
    like = models.BooleanField(default=True)


class BookMarck(models.Model):
    post = models.ManyToManyField(Posts)
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    
    def __str__(self):
        return self.user.user.username
