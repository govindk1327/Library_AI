from django.core.management.base import BaseCommand
import asyncio
from recommendations.pipeline import run_recommendation_pipeline
import sys

class Command(BaseCommand):
    help = "Test HyperClovaX recommendation pipeline manually"

    def add_arguments(self, parser):
        parser.add_argument("query", type=str, help="Natural language book recommendation query")
    
    if sys.platform.startswith("win"):
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

    def handle(self, *args, **options):
        query = options["query"]
        result = asyncio.run(run_recommendation_pipeline(query))
        self.stdout.write(self.style.SUCCESS("✅ Pipeline result:"))
        self.stdout.write(str(result))
