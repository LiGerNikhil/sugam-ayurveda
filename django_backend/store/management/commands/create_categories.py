from django.core.management.base import BaseCommand
from store.models import Category

class Command(BaseCommand):
    help = 'Create categories with images for Sugam Ayurveda'

    def handle(self, *args, **options):
        categories_data = [
            {
                'id': 'diabetes',
                'name': 'Diabetes Care',
                'description': 'Natural remedies and supplements for diabetes management and blood sugar control'
            },
            {
                'id': 'liver-care',
                'name': 'Liver & Gallbladder Care',
                'description': 'Ayurvedic formulations for liver detoxification and gallbladder health'
            },
            {
                'id': 'piles-care',
                'name': 'Piles & Hemorrhoids Care',
                'description': 'Effective Ayurvedic treatments for piles, fissures, and hemorrhoids'
            },
            {
                'id': 'joint-care',
                'name': 'Joint & Bone Care',
                'description': 'Natural solutions for joint pain, arthritis, and bone health'
            },
            {
                'id': 'mens-health',
                'name': "Men's Health",
                'description': 'Ayurvedic supplements for male vitality, stamina, and sexual wellness'
            },
            {
                'id': 'digestive-care',
                'name': 'Digestive Care',
                'description': 'Natural remedies for digestion, gas, acidity, and gut health'
            },
            {
                'id': 'cough-cold',
                'name': 'Cough, Cold & Immunity',
                'description': 'Ayurvedic formulations for respiratory health and immune system support'
            },
            {
                'id': 'sleep-stress',
                'name': 'Sleep & Stress Relief',
                'description': 'Natural remedies for better sleep, stress management, and migraine relief'
            },
            {
                'id': 'superfoods',
                'name': 'Superfoods & Daily Health',
                'description': 'Nutrient-rich Ayurvedic superfoods for daily wellness and nutrition'
            }
        ]

        created_count = 0
        updated_count = 0

        for category_data in categories_data:
            category, created = Category.objects.update_or_create(
                id=category_data['id'],
                defaults={
                    'name': category_data['name'],
                    'description': category_data['description']
                }
            )
            
            if created:
                created_count += 1
                self.stdout.write(self.style.SUCCESS(f'Created category: {category.name}'))
            else:
                updated_count += 1
                self.stdout.write(self.style.WARNING(f'Updated category: {category.name}'))

        self.stdout.write(self.style.SUCCESS(
            f'\nCategories created/updated successfully!\n'
            f'Created: {created_count}\n'
            f'Updated: {updated_count}\n'
            f'Total categories: {Category.objects.count()}'
        ))
