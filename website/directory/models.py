import qrcode
import functools
from PIL import Image, ImageDraw
from io import BytesIO
from django.db import models
from django.core.files import File

# from django.contrib.auth.models import User
from django.urls import reverse
from django_prometheus.models import ExportModelOperationsMixin
from website.settings import DJANGO_BASE_URL, COMPANY_LOGO
from accounts.models import CustomUser


# Create your models here.
class BaseTimestampedModel(models.Model):
    created_at = models.DateTimeField("Time Record Created", auto_now_add=True)
    updated_at = models.DateTimeField("Time Record Updated", auto_now=True)

    class Meta:
        abstract = True


class BaseUserTrackedModel(models.Model):
    created_by = models.ForeignKey(
        CustomUser,
        on_delete=models.SET_NULL,
        related_name="%(app_label)s_%(class)s_created_by",
        null=True,
        blank=True,
    )
    updated_by = models.ForeignKey(
        CustomUser,
        on_delete=models.SET_NULL,
        related_name="%(app_label)s_%(class)s_updated_by",
        null=True,
        blank=True,
    )

    class Meta:
        abstract = True


class RecordMixin(BaseTimestampedModel, BaseUserTrackedModel):
    is_active = models.BooleanField("If Record Is Active", default=True, db_index=True)

    class Meta:
        abstract = True


class Staff(ExportModelOperationsMixin("staff"), RecordMixin):
    first_name = models.CharField(
        verbose_name="First Name", max_length=200, db_index=True, null=False
    )
    last_name = models.CharField(
        verbose_name="Last Name", max_length=200, db_index=True, null=False
    )
    title = models.CharField(max_length=200, null=True, default="", blank=True)
    email = models.EmailField(db_index=True, unique=True, null=False)
    phone = models.CharField(max_length=200, db_index=True)
    office = models.CharField(max_length=200, null=True, blank=True)
    company_url = models.URLField(
        verbose_name="Company Website", max_length=200, null=True, blank=True
    )
    bio = models.TextField()
    slug = models.SlugField(
        verbose_name="WebLink Slug",
        max_length=100,
        unique=True,
        null=True,
        db_index=True,
    )
    image = models.ImageField(
        verbose_name="Profile Image", upload_to="staff_images", blank=True
    )
    qrcode_img_vcard = models.ImageField(
        verbose_name="Contact Card QRcode", upload_to="vcard-qrcodes", blank=True
    )

    def __str__(self):
        return f"{self.title} {self.first_name} {self.last_name}"

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"

    @property
    def contact_card_data(self):
        # Format the data as a vCard (Virtual Contact File)
        vcf = [
            "BEGIN:VCARD",
            "VERSION:3.0",
            f"N:{self.full_name}",
            f"TITLE:{self.title}",
            f"TEL:{self.phone}",
            f"EMAIL:{self.email}",
            f"URL;type=pref:{DJANGO_BASE_URL}{reverse('staff_details',args=[self.slug])}",
        ]
        if self.office:
            vcf.append(f"ORG:{self.office}")
        if self.company_url:
            # Because the field is not mandatory, dont want to add None
            vcf.append(f"URL;type=company:{self.company_url}")
        vcf.append("END:VCARD")
        return "\n".join(vcf)

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
        logo = load_logo()

        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_H,
            box_size=10,
            border=4,
        )
        qr.add_data(self.contact_card_data)
        qr.make(fit=True)

        img = qr.make_image(fill_color="black", back_color="white")

        # Paste the logo in the middle of the QR code
        logo_position = (
            (img.size[0] - logo.size[0]) // 2,
            (img.size[1] - logo.size[1]) // 2,
        )
        img.paste(logo, logo_position, mask=logo)

        # Create a BytesIO object to hold the image data
        img_buffer = BytesIO()
        img.save(img_buffer, format="PNG")
        img_buffer.seek(0)

        # Delete the old image if it exists
        if self.qrcode_img_vcard:
            self.qrcode_img_vcard.delete(save=False)

        # Save the image data to the qrcode_image field
        self.qrcode_img_vcard.save(
            f"{self.last_name}-{self.first_name}-VCard-QRcode.png",
            File(img_buffer),
            save=False,
        )


@functools.cache
def load_logo(base_width: int = 200):
    logo = Image.open(COMPANY_LOGO)
    # Resize the logo to be a max of base_width wide and proportional height
    w_percent = base_width / float(logo.size[0])
    h_size = int((float(logo.size[1]) * float(w_percent)))
    logo = logo.resize(
        (base_width, h_size)
    )  # , Image.Resampling.LANCZOS) #let resampling off for now

    transparent_background = Image.new("RGBA", logo.size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(transparent_background)
    draw.ellipse((0, 0, logo.size[0], logo.size[1]), fill=(255, 255, 255, 255))
    transparent_background.paste(logo, mask=logo)

    logo = transparent_background

    return logo
