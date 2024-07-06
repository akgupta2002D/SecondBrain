from .models import LifeGoal


def get_all_life_goals_sync():
    return list(LifeGoal.objects.all())


def get_projects_for_life_goal_sync(life_goal):
    return list(life_goal.projects.all())
