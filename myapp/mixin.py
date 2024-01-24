class CustomUserMixin: 
    def __str__(self):
        return f"{self.Nom} {self.Prenom}"

    def save(self, *args, **kwargs):
        self.user.first_name = self.prenom
        self.user.last_name = self.nom
        self.user.username = f"{self.nom} {self.prenom}"
        self.user.email = self.email
        self.user.save() 
        super().save(*args, **kwargs)