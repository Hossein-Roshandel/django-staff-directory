import qrcode
from io import BytesIO
from django.db import models
from django.core.files import File
from django.contrib.auth.models import User

# Create your models here.
class BaseTimestampedModel(models.Model):
    created_at = models.DateTimeField("Time Record Created", auto_now_add=True)
    updated_at = models.DateTimeField("Time Record Updated", auto_now=True)

    class Meta:
        abstract = True

class BaseUserTrackedModel(models.Model):
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, related_name="%(app_label)s_%(class)s_created_by", null=True, blank=True)
    updated_by = models.ForeignKey(User, on_delete=models.SET_NULL, related_name="%(app_label)s_%(class)s_updated_by", null=True, blank=True)

    class Meta:
        abstract = True

class RecordMixin(BaseTimestampedModel,BaseUserTrackedModel):
    is_active = models.BooleanField("If Record Is Active", default=True, db_index=True)
    
    class Meta:
        abstract = True

class Staff(RecordMixin):
    fname = models.CharField(verbose_name="First Name", max_length=200,db_index=True, null=False)
    lname = models.CharField(verbose_name="Last Name",max_length=200,db_index=True, null=False)
    title = models.CharField(max_length=200,null=True, default="")
    email = models.EmailField(db_index=True, unique=True, null=False)
    phone = models.CharField(max_length=200,db_index=True)
    office = models.CharField(max_length=200, null=True)
    bio = models.TextField()
    image = models.ImageField(verbose_name="Profile Image", upload_to='staff_images', blank=True)
    qrcode_image = models.ImageField(verbose_name="Contact Card QRcode",upload_to='qrcode_images', blank=True)


    def __str__(self):
        return f"{self.title} {self.fname} {self.lname}"
    
    @property
    def full_name(self):
        return f"{self.fname} {self.lname}"
    
    @property
    def contact_card_data(self):
        # Format the data as a vCard (Virtual Contact File)
        contac_card = f"BEGIN:VCARD\n" \
                  f"VERSION:3.0\n" \
                  f"N:{self.full_name} ({self.title})\n" \
                  f"ORG:{self.office}\n" \
                    f"TEL:{self.phone}\n" \
                    f"EMAIL:{self.email}\n" \
                    f"END:VCARD"
        return contac_card
    
    @property
    def any_contact_data_changed(self):
        if self.pk:
            old_data = Staff.objects.get(pk=self.pk).contact_card_data
            return old_data != self.contact_card_data
        return True
    
    
    def save(self, *args, **kwargs):
        if self.any_contact_data_changed:
            self.create_qrcode()
        super().save(*args, **kwargs)

    
    def create_qrcode(self):
        """
        Automatically generate and update the QR code image
        """
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data(self.contact_card_data)
        qr.make(fit=True)

        img = qr.make_image(fill_color="black", back_color="white")
        # Create a BytesIO object to hold the image data
        img_buffer = BytesIO()
        img.save(img_buffer, format='PNG')
        img_buffer.seek(0)

        # Save the image data to the qrcode_image field
        self.qrcode_image.save(f"{self.lname}_{self.fname}_qrcode.png", 
                               File(img_buffer), 
                               save=False)

    


