from django.core.management.base import BaseCommand
from octofit_tracker.models import User, Team, Activity, Leaderboard, Workout
from octofit_tracker.test_data import test_data

class Command(BaseCommand):
    help = 'Populate the database with test data for users, teams, activities, leaderboard, and workouts'

    def handle(self, *args, **kwargs):
        # Clear existing data
        User.objects.all().delete()
        Team.objects.all().delete()
        Activity.objects.all().delete()
        Leaderboard.objects.all().delete()
        Workout.objects.all().delete()

        # Populate users
        users = [User(**user) for user in test_data['users']]
        User.objects.bulk_create(users)

        # Save teams without members first
        teams = [Team.objects.create(name=team['name']) for team in test_data['teams']]

        # Assign members to teams after saving
        for i, team in enumerate(teams):
            team.members.add(*users[i::2])  # Assign every other user to each team
            team.save()

        # Populate activities
        activities = [
            Activity(**{**activity, 'user': users[i % len(users)]})
            for i, activity in enumerate(test_data['activities'])
        ]
        Activity.objects.bulk_create(activities)

        # Populate leaderboard
        leaderboard = [
            Leaderboard(**{**entry, 'user': users[i % len(users)]})
            for i, entry in enumerate(test_data['leaderboard'])
        ]
        Leaderboard.objects.bulk_create(leaderboard)

        # Populate workouts
        workouts = [Workout(**workout) for workout in test_data['workouts']]
        Workout.objects.bulk_create(workouts)

        self.stdout.write(self.style.SUCCESS('Successfully populated the database with test data.'))

