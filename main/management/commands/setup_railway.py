from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from main.models import CV
from django.utils import timezone

class Command(BaseCommand):
    help = 'Set up Railway database with sample data and admin user'

    def handle(self, *args, **options):
        self.stdout.write('Setting up Railway database...')
        
        # Create admin user
        if not User.objects.filter(username='admin').exists():
            admin_user = User.objects.create(
                username='admin',
                email='admin@cvproject.com',
                password=make_password('admin123'),
                is_staff=True,
                is_superuser=True,
                first_name='Admin',
                last_name='User'
            )
            self.stdout.write(self.style.SUCCESS(f'Created admin user: admin/admin123'))
        else:
            self.stdout.write('Admin user already exists')
        
        # Create sample CVs - ensure we have at least 3 CVs
        cv_count = CV.objects.count()
        self.stdout.write(f'Current CV count: {cv_count}')
        
        # Create additional CVs if needed
        if cv_count < 3:
            # Sample CV 1 (John Doe)
            if not CV.objects.filter(firstname='John', lastname='Doe').exists():
                cv1 = CV.objects.create(
                    firstname='John',
                    lastname='Doe',
                    bio='Experienced software developer with 5+ years in web development. Passionate about creating scalable and maintainable code.',
                    skills='Python, Django, JavaScript, React, PostgreSQL, Docker, AWS',
                    projects='Built a full-stack e-commerce platform using Django and React. Implemented CI/CD pipeline with GitHub Actions. Developed RESTful APIs for mobile applications.',
                    contacts='john.doe@email.com\n+1 (555) 123-4567\nLinkedIn: linkedin.com/in/johndoe'
                )
                self.stdout.write('Created CV: John Doe')
            
            # Sample CV 2 (Jane Smith)
            if not CV.objects.filter(firstname='Jane', lastname='Smith').exists():
                cv2 = CV.objects.create(
                    firstname='Jane',
                    lastname='Smith',
                    bio='Full-stack developer specializing in modern web technologies. Strong focus on user experience and performance optimization.',
                    skills='JavaScript, TypeScript, React, Node.js, MongoDB, GraphQL, Kubernetes',
                    projects='Led development of a real-time chat application. Optimized database queries reducing load times by 60%. Implemented microservices architecture.',
                    contacts='jane.smith@email.com\n+1 (555) 987-6543\nGitHub: github.com/janesmith'
                )
                self.stdout.write('Created CV: Jane Smith')
            
            # Sample CV 3 (Alex Johnson)
            if not CV.objects.filter(firstname='Alex', lastname='Johnson').exists():
                cv3 = CV.objects.create(
                    firstname='Alex',
                    lastname='Johnson',
                    bio='DevOps engineer with expertise in cloud infrastructure and automation. Passionate about building reliable and scalable systems.',
                    skills='Docker, Kubernetes, AWS, Terraform, Python, Bash, Jenkins',
                    projects='Migrated legacy infrastructure to Kubernetes. Implemented automated deployment pipeline. Reduced infrastructure costs by 40%.',
                    contacts='alex.johnson@email.com\n+1 (555) 456-7890\nTwitter: @alexjohnson'
                )
                self.stdout.write('Created CV: Alex Johnson')
            
            final_count = CV.objects.count()
            self.stdout.write(self.style.SUCCESS(f'Created {final_count - cv_count} additional CVs'))
        else:
            self.stdout.write(f'Database already contains {cv_count} CVs (sufficient)')
        
        self.stdout.write(self.style.SUCCESS('Railway database setup completed successfully!'))
        self.stdout.write('Admin credentials: admin/admin123')
        self.stdout.write(f'Total CVs in database: {CV.objects.count()}')
