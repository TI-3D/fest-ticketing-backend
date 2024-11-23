import cloudinary
from app.core.config import settings

class CloudinaryService:
    def __init__(self):
        # Konfigurasi Cloudinary
        self.cloudinary = cloudinary
        self.cloudinary.config(
            cloud_name=settings.CLOUDINARY_CLOUD_NAME,
            api_key=settings.CLOUDINARY_API_KEY,
            api_secret=settings.CLOUDINARY_API_SECRET
        )
    
    def upload(self, file_path, options=None, width=None, height=None):
        """
        Upload gambar dengan ID acak dan optimasi untuk perangkat mobile,
        serta menentukan lebar dan tinggi gambar.
        :param file_path: Lokasi file gambar yang ingin di-upload.
        :param options: Opsi tambahan untuk upload (misalnya folder, public_id, dll.).
        :param width: Lebar gambar yang diinginkan (opsional).
        :param height: Tinggi gambar yang diinginkan (opsional).
        :return: Response dari Cloudinary setelah upload.
        """
        if options is None:
            options = {}

        # Menambahkan optimasi gambar untuk perangkat mobile
        options.update({
            'quality': 'auto',             # Kualitas otomatis (kompresi gambar)
            'fetch_format': 'auto',        # Format gambar otomatis (misalnya WebP)
            'dpr': 'auto',                 # Menyesuaikan resolusi gambar untuk perangkat dengan densitas tinggi
            'aspect_ratio': '16:9',        # Memastikan rasio aspek tetap konsisten
            'background': 'auto',          # Menjaga latar belakang gambar tetap transparan (jika ada)
            'public_id': cloudinary.utils.random_public_id()  # Generate public_id acak
        })

        # Menentukan ukuran lebar dan tinggi jika ada
        if width:
            options['width'] = width
        if height:
            options['height'] = height
        
        try:
            # Upload gambar ke Cloudinary dengan opsi yang telah ditentukan
            response = self.cloudinary.uploader.upload(file_path, **options)
            return response
        except cloudinary.exceptions.Error as e:
            print(f"Error uploading image: {e}")
            return None

    def get_mobile_optimized_url(self, public_id, width=None, height=None):
        """
        Mendapatkan URL gambar yang dioptimalkan untuk perangkat mobile,
        serta menentukan lebar dan tinggi gambar sesuai kebutuhan.
        :param public_id: ID unik gambar yang telah di-upload ke Cloudinary.
        :param width: Lebar gambar yang diinginkan (opsional).
        :param height: Tinggi gambar yang diinginkan (opsional).
        :return: URL Cloudinary yang dioptimalkan untuk perangkat mobile.
        """
        options = {
            'quality': 'auto',             # Kualitas otomatis
            'fetch_format': 'auto',        # Format gambar otomatis (misalnya WebP)
            'dpr': 'auto',                 # Menyesuaikan resolusi untuk perangkat dengan densitas tinggi
        }

        # Menentukan lebar dan tinggi jika ada
        if width:
            options['width'] = width
        if height:
            options['height'] = height
        
        return self.cloudinary.utils.cloudinary_url(public_id, **options, secure=True)

    def delete_image(self, public_id):
        """
        Menghapus gambar dari Cloudinary berdasarkan public_id.
        :param public_id: ID unik gambar yang ingin dihapus.
        :return: Response dari Cloudinary setelah penghapusan.
        """
        try:
            # Menghapus gambar berdasarkan public_id
            response = self.cloudinary.uploader.destroy(public_id)
            return response
        except cloudinary.exceptions.Error as e:
            print(f"Error deleting image: {e}")
            return None
