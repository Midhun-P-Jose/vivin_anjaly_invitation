import os
import sys
import re
from pathlib import Path
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'wedding_project.settings')
django.setup()

from invitation.models import GalleryMedia

def run():
    GalleryMedia.objects.all().delete()
    
    pics_dir = Path('media/vivn_anjaly_pics')
    if not pics_dir.exists():
        print("Directory does not exist:", pics_dir)
        return
        
    def sort_order(name):
        m = re.search(r'(\d+)', name)
        return int(m.group(1)) if m else 999

    files = [f.name for f in pics_dir.iterdir() if f.suffix.lower() in ['.jpeg', '.jpg', '.png']]
    files.sort(key=sort_order)
    
    for i, fname in enumerate(files, start=1):
        rel_path = f"vivn_anjaly_pics/{fname}"
        GalleryMedia.objects.create(
            title="Vivin & Anjaly",
            media_type="photo",
            image=rel_path,
            order=i,
            is_featured=True,
            category="all"
        )
        print(f"Added #{i}: {rel_path}")
        
    print(f"✅ Successfully seeded {len(files)} photos to GalleryMedia.")

if __name__ == '__main__':
    run()
