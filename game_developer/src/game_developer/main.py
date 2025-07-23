#!/usr/bin/env python
import sys
import yaml
import warnings

from datetime import datetime

from game_developer.crew import GameDeveloper

warnings.filterwarnings("ignore", category=SyntaxWarning, module="pysbd")

def run():
    """
    Run the crew.
    """
    try:
        print("## Welcome to the Game Crew")
        print('-------------------------------')

        with open('src/game_developer/config/gamedesign.yaml', 'r', encoding='utf-8') as file:
            examples = yaml.safe_load(file)

        inputs = {
            'game' :  examples['example3_snake']
        }
        game= GameDeveloper().crew().kickoff(inputs=inputs)

        print("\n\n########################")
        print("## Here is the result")
        print("########################\n")
        print("final code for the game:")
        print(game)
    except Exception as e:
        raise Exception(f"An error occurred while running the crew: {e}")


def train():
    """
    Train the crew for a given number of iterations.
    """
    inputs = {
        "topic": "AI LLMs",
        'current_year': str(datetime.now().year)
    }
    try:
        GameDeveloper().crew().train(n_iterations=int(sys.argv[1]), filename=sys.argv[2], inputs=inputs)

    except Exception as e:
        raise Exception(f"An error occurred while training the crew: {e}")

def replay():
    """
    Replay the crew execution from a specific task.
    """
    try:
        GameDeveloper().crew().replay(task_id=sys.argv[1])

    except Exception as e:
        raise Exception(f"An error occurred while replaying the crew: {e}")

def test():
    """
    Test the crew execution and returns the results.
    """
    inputs = {
        "topic": "AI LLMs",
        "current_year": str(datetime.now().year)
    }
    
    try:
        GameDeveloper().crew().test(n_iterations=int(sys.argv[1]), eval_llm=sys.argv[2], inputs=inputs)

    except Exception as e:
        raise Exception(f"An error occurred while testing the crew: {e}")
