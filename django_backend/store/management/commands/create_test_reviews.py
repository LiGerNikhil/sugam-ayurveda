from django.core.management.base import BaseCommand
from store.models import Review
from django.utils import timezone
import random

class Command(BaseCommand):
    help = 'Create test reviews for the homepage'

    def handle(self, *args, **options):
        # Clear existing reviews
        Review.objects.all().delete()
        
        test_reviews = [
            {
                'name': 'Priya Sharma',
                'email': 'priya.sharma@email.com',
                'title': 'Amazing Ayurvedic Products!',
                'content': 'I have been using Sugam Ayurveda products for the past 3 months and the results are incredible. My skin has never looked better and I feel so much more energetic. The quality is outstanding and the customer service is excellent.',
                'rating': 5,
                'is_anonymous': False
            },
            {
                'name': 'Rahul Verma',
                'email': 'rahul.verma@email.com',
                'title': 'Life-Changing Experience',
                'content': 'These products have completely transformed my health. I was struggling with stress and sleep issues, but after using their herbal remedies, I feel like a new person. Highly recommend to everyone!',
                'rating': 5,
                'is_anonymous': False
            },
            {
                'name': 'Anjali Patel',
                'email': 'anjali.patel@email.com',
                'title': 'Great Quality Products',
                'content': 'Very satisfied with my purchase. The products are authentic and the results are visible within weeks. Packaging is also very good and delivery was on time.',
                'rating': 4,
                'is_anonymous': False
            },
            {
                'name': 'Amit Kumar',
                'email': 'amit.kumar@email.com',
                'title': 'Good but could be better',
                'content': 'The products are good quality but the prices are a bit high. However, the effectiveness makes up for the cost. Customer support was helpful when I had questions.',
                'rating': 4,
                'is_anonymous': False
            },
            {
                'name': 'Neha Singh',
                'email': 'neha.singh@email.com',
                'title': 'Excellent Service!',
                'content': 'I am so impressed with the quality and service. The team guided me through the product selection and helped me choose exactly what I needed. Results have been amazing!',
                'rating': 5,
                'is_anonymous': False
            },
            {
                'name': 'Vikram Malhotra',
                'email': 'vikram.m@email.com',
                'title': 'Worth Every Penny',
                'content': 'Initially I was skeptical about the price, but after seeing the results, I can say it\'s worth every penny. These are genuine Ayurvedic products that actually work.',
                'rating': 5,
                'is_anonymous': False
            },
            {
                'name': 'Sunita Reddy',
                'email': 'sunita.r@email.com',
                'title': 'Very Effective',
                'content': 'I have tried many brands but Sugam Ayurveda stands out. The products are pure, effective, and the results are long-lasting. Will definitely order again.',
                'rating': 4,
                'is_anonymous': False
            },
            {
                'name': 'Rajesh Gupta',
                'email': 'rajesh.g@email.com',
                'title': 'Good Products',
                'content': 'Nice products with good quality. The herbal supplements have helped me with my digestion issues. Overall satisfied with the experience.',
                'rating': 4,
                'is_anonymous': False
            },
            {
                'name': 'Meera Joshi',
                'email': 'meera.j@email.com',
                'title': 'Love the Natural Approach',
                'content': 'Finally found authentic Ayurvedic products! Love that everything is natural and chemical-free. My family has been using these products and we all see positive changes.',
                'rating': 5,
                'is_anonymous': False
            },
            {
                'name': 'Karan Sharma',
                'email': 'karan.s@email.com',
                'title': 'Satisfied Customer',
                'content': 'Great experience from start to finish. Products are effective, shipping is fast, and customer service is responsive. What more could you ask for?',
                'rating': 5,
                'is_anonymous': False
            },
            {
                'name': 'Anonymous User',
                'email': 'anonymous@email.com',
                'title': 'Helped with my anxiety',
                'content': 'The stress relief products have been a game-changer for me. I feel much calmer and more focused. Thank you Sugam Ayurveda for these amazing products!',
                'rating': 5,
                'is_anonymous': True
            },
            {
                'name': 'Anonymous User',
                'email': 'anonymous2@email.com',
                'title': 'Good for skin problems',
                'content': 'I had persistent skin issues for years. After using their skincare products for 2 months, my skin is clear and glowing. So grateful!',
                'rating': 4,
                'is_anonymous': True
            }
        ]
        
        created_count = 0
        for review_data in test_reviews:
            review = Review.objects.create(
                name=review_data['name'],
                email=review_data['email'],
                title=review_data['title'],
                content=review_data['content'],
                rating=review_data['rating'],
                is_anonymous=review_data['is_anonymous'],
                is_approved=True,
                created_at=timezone.now() - timezone.timedelta(days=random.randint(1, 30))
            )
            created_count += 1
        
        self.stdout.write(
            self.style.SUCCESS(f'Successfully created {created_count} test reviews!')
        )
