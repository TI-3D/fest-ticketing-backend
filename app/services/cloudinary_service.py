import cloudinary
from cloudinary.uploader import upload
from cloudinary.api import delete_resources_by_prefix
from app.core.config import settings

class CloudinaryService:
    def __init__(self):
        cloudinary.config(
            cloud_name=settings.CLOUDINARY_CLOUD_NAME,
            api_key=settings.CLOUDINARY_API_KEY,
            api_secret=settings.CLOUDINARY_API_SECRET
        )

    def upload_image(self, file_path, folder_name=None, width=None, height=None, crop=None, options=None):
        """
        Upload an image to Cloudinary with optional transformations.
        :param file_path: Path to the image file.
        :param folder_name: The folder to upload the image to.
        :param width: The width of the image (optional).
        :param height: The height of the image (optional).
        :param crop: The crop mode (optional).
        :param options: Additional options for uploading.
        :return: Cloudinary upload response.
        """
        if options is None:
            options = {}

        # Only add background if using a crop mode that supports it
        if crop in ['fill', 'pad']:
            options['background'] = 'auto'

        # Add image transformations (optional)
        if width:
            options['width'] = width
        if height:
            options['height'] = height
        if crop:
            options['crop'] = crop

        if folder_name:
            options['folder'] = folder_name

        try:
            # Upload the image to Cloudinary
            response = upload(file_path, **options)
            return response  # Return the Cloudinary response
        except cloudinary.exceptions.Error as e:
            print(f"Error uploading image: {e}")
            return None

    def get_optimized_url(self, public_id, width=None, height=None):
        """
        Get an optimized URL for the image.
        :param public_id: The Cloudinary public ID of the image.
        :param width: The width (optional).
        :param height: The height (optional).
        :return: Optimized URL for the image.
        """
        options = {
            'quality': 'auto',
            'fetch_format': 'auto',
            'dpr': 'auto',
        }

        if width:
            options['width'] = width
        if height:
            options['height'] = height

        # Generate the URL
        return cloudinary.utils.cloudinary_url(public_id, **options, secure=True)

    def delete_image(self, public_id, folder_name=None):
        """
        Delete an image from Cloudinary using the public ID.
        :param public_id: The Cloudinary public ID of the image.
        :param folder_name: The folder where the image is stored (optional).
        :return: Cloudinary deletion response.
        """
        try:
            # If a folder_name is provided, ensure public_id matches the folder structure
            if folder_name:
                # Folder name should be part of the public_id, so prepend it if necessary
                public_id = f"{folder_name}/{public_id}" if not public_id.startswith(folder_name) else public_id

            # Delete the image using its public_id
            print(f"Deleting image with public ID: {public_id}")
            response = cloudinary.uploader.destroy(public_id)

            # Log the result of the deletion
            if response.get('result') == 'ok':
                print(f"Successfully deleted image with public ID: {public_id}")
            else:
                print(f"Failed to delete image with public ID: {public_id}")
            return response
        except cloudinary.exceptions.Error as e:
            print(f"Error deleting image: {e}")
            return None
        
    def delete_folder(self, folder_name):
        """
        Delete a folder and its contents from Cloudinary.
        :param folder_name: The folder name to delete.
        :return: Cloudinary deletion response.
        """
        try:
            response = delete_resources_by_prefix(folder_name)
            return response
        except cloudinary.exceptions.Error as e:
            print(f"Error deleting folder: {e}")
            return None
