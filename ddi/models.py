from django.db import models

# Create your models here.

# class Router(models.Model):
#     config = models.CharField(max_length=15)
#     value = models.CharField(max_length=15)

#     def __str__(self):
#         return self.config

class OS(models.Model):

    name = models.CharField(max_length=25)

    def __str__(self):
        return self.name   

class Subnet(models.Model):
    netmask = models.CharField(max_length=15)
    ip_network = models.CharField(max_length=15)
    ip_broadcast = models.CharField(max_length=15)
    description = models.TextField()

    def __str__(self):
        return self.ip_network

class Ip_Address(models.Model):

    ip_address = models.CharField(max_length=15)
    hostname = models.CharField(max_length=25)
    description = models.TextField()
    subnet = models.ForeignKey(Subnet, on_delete=models.CASCADE)
    os = models.ForeignKey(OS, on_delete=models.SET_NULL, null=True)
    username = models.CharField(max_length=15)
    password = models.TextField()

    def __str__(self):
        return self.ip_address

class Dhcp_Server(models.Model):

    name = models.CharField(max_length=15)
    subnet = models.CharField(max_length=18)
    interface = models.CharField(max_length=7)
    ip_start = models.CharField(max_length=15)
    ip_end = models.CharField(max_length=15)
    gateway = models.CharField(max_length=15)
    dns = models.CharField(max_length=31)
    
    idm_network = models.CharField(max_length=5)
    idm_pool = models.CharField(max_length=5)
    idm_dhcp = models.CharField(max_length=5)

    def __str__(self):
        return self.name

class Dhcp_Static(models.Model):

    id = models.CharField(max_length=6, primary_key=True)
    name = models.CharField(max_length=20)
    mac = models.CharField(max_length=30)
    ip = models.CharField(max_length=15)
    description = models.TextField()

    def __str__(self):
        return self.name

class Domain(models.Model):

    domain = models.CharField(max_length=20)
    ip = models.CharField(max_length=15)
    description = models.TextField()

    def __str__(self):
        return self.domain

class Subdomain(models.Model):

    id = models.CharField(max_length=6, primary_key=True)
    domain = models.ForeignKey(Domain, on_delete=models.CASCADE)
    subdomain = models.CharField(max_length=20)
    ip = models.CharField(max_length=15)
    description = models.TextField()

    def __str__(self):
        return self.subdomain