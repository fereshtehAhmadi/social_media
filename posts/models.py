from django.db import models
from accounts.models import User


class Posts(models.Model):
    content = models.TextField()
    views = models.IntegerField(default=0)
    create = models.DateTimeField(auto_now_add=True)
    update = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    
    def __str__(self):
        return f'{self.id}'


class Gallery(models.Model):
    image = models.ImageField(upload_to='posts/')
    post = models.ForeignKey(Posts, on_delete=models.CASCADE)
    selected = models.BooleanField(default=False)
    
    def __str__(self):
        return f'{self.id}'


class LikePost(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Posts, on_delete=models.CASCADE)
    like = models.BooleanField(default=True)
    
    def __str__(self):
        return self.user.username


class Comment(models.Model):
    content = models.TextField()
    create = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Posts, on_delete=models.CASCADE)
    
    def __str__(self):
        return str(self.id)


class LikeComment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE)
    like = models.BooleanField(default=True)
    
    def __str__(self):
        return self.user.username


class ReplyComment(models.Model):
    content = models.TextField()
    create = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE)
    
    def __str__(self):
        return str(self.id)


class LikeReply(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    reply = models.ForeignKey(ReplyComment, on_delete=models.CASCADE)
    like = models.BooleanField(default=True)
    
    def __str__(self):
        return self.user.username


class BookMarck(models.Model):
    post = models.ManyToManyField(Posts)
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    
    def __str__(self):
        return self.user.username
