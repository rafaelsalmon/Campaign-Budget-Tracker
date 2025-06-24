
from django.core.management.base import BaseCommand, CommandError
from ads.models import Campaign


class Command(BaseCommand):
    help = "Simulates a spend event for a campaign"

    def add_arguments(self, parser):
        parser.add_argument("campaign_id", type=int, help="ID of the campaign")
        parser.add_argument("amount", type=float, help="Amount to spend")

    def handle(self, *args, **options):
        campaign_id = options["campaign_id"]
        amount = options["amount"]

        try:
            campaign = Campaign.objects.select_related("brand").get(pk=campaign_id)
        except Campaign.DoesNotExist:
            raise CommandError(f"Campaign with ID {campaign_id} does not exist.")

        # Update spend
        campaign.daily_spend += amount
        campaign.brand.current_daily_spend += amount
        campaign.brand.current_monthly_spend += amount

        # Check for budget limits
        if (
            campaign.brand.current_daily_spend > campaign.brand.daily_budget or
            campaign.brand.current_monthly_spend > campaign.brand.monthly_budget
        ):
            campaign.is_active = False

        # Save all changes
        campaign.brand.save()
        campaign.save()

        self.stdout.write(self.style.SUCCESS(
            f"Successfully simulated ${amount:.2f} spend for Campaign {campaign.name} (ID {campaign_id})"
        ))
