import csv
from pathlib import Path

from django.core.management.base import BaseCommand

from explainer.models import CodeSample


class Command(BaseCommand):
    help = "Load sample snippets from data/samples.csv"

    def handle(self, *args, **options):
        path = Path(__file__).resolve().parents[2] / "data" / "samples.csv"
        count = 0
        with open(path, newline="", encoding="utf-8") as f:
            for row in csv.DictReader(f):
                row["code"] = row["code"].replace("\\n", "\n")
                _, created = CodeSample.objects.get_or_create(
                    title=row["title"], defaults=row
                )
                count += int(created)
        self.stdout.write(self.style.SUCCESS(f"Loaded {count} new samples"))