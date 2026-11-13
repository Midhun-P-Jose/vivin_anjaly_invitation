import os
import pathlib

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'wedding_project.settings')
import django
django.setup()

from invitation.models import GalleryMedia

pics_dir = pathlib.Path('media/vivn_anjaly_pics')
image_files = sorted(pics_dir.glob('*.jpeg')) + sorted(pics_dir.glob('*.jpg')) + sorted(pics_dir.glob('*.png'))

for i, img_path in enumerate(image_files, start=1):
    rel_path = f'vivn_anjaly_pics/{img_path.name}'
    if not GalleryMedia.objects.filter(image_file=rel_path).exists():
        GalleryMedia.objects.create(
            title=f'Vivn Anjaly Photo {i}',
            media_type='image_file',
            image_file=rel_path,
            caption='',
            category='pre_wedding',
            is_featured=True,
            order=i,
        )
        print(f'Added {rel_path}')
    else:
        print(f'Skipped {rel_path}, already exists')

# Add video if exists
video_path = pathlib.Path('media/video/cute_highlight.mp4')
if video_path.exists():
    rel_video = 'video/cute_highlight.mp4'
    if not GalleryMedia.objects.filter(video_file=rel_video).exists():
        GalleryMedia.objects.create(
            title='Cute Highlight',
            media_type='video_file',
            video_file=rel_video,
            caption='A short montage of our cutest moments.',
            category='pre_wedding',
            is_featured=True,
            order=999,
        )
        print('Added video entry')
    else:
        print('Video entry already exists')
else:
    print('Video file not found, skipping video entry')

