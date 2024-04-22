from django.db import models
from datetime import datetime

class TicketModel(models.Model):
    code1 = models.CharField(max_length=100)
    ticket_name = models.CharField(max_length=100)
    booking_code = models.CharField(max_length=100)
    ticket_price = models.CharField(max_length=100)
    ticket_date = models.CharField(max_length=100)
    expiration_date = models.CharField(max_length=100)
    code2 = models.CharField(max_length=100)
    code3 = models.CharField(max_length=100, default='default_value')



    def __str__(self):
        return f"{self.ticket_name} {self.code1}"