from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task, before_kickoff, after_kickoff
from crewai_tools import ScrapeWebsiteTool
from pydantic import BaseModel, Field
from typing import Dict, List

# If you want to run a snippet of code before or after the crew starts,
# you can use the @before_kickoff and @after_kickoff decorators
# https://docs.crewai.com/concepts/crews#example-crew-class-with-decorators

class JobPostingModel(BaseModel):
    """Schema for job posting data"""
    region: str = Field(description="Region or area where the job is located", default=None)
    role: str = Field(description="Specific role or function within the job category", default=None)
    job_title: str = Field(description="Title of the job position", default=None)
    experience_years: str = Field(description="Experience required for the position", default=None)
    job_link: str = Field(description="Link to the job posting", default=None)


class IndustryTrend(BaseModel):
    """Schema for industry trend data"""
    industry: str = Field(description="Industry name", default=None)
    avg_salary: float = Field(description="Average salary in the industry", default=None)
    growth_rate: float = Field(description="Growth rate of the industry", default=None)
    demand_level: str = Field(description="Demand level in the industry", default=None)
    top_skills: List[str] = Field(description="Top skills in demand for this industry", default=None)

@CrewBase
class JobHunting():
    """JobHunting crew"""

    # Learn more about YAML configuration files here:
    # Agents: https://docs.crewai.com/concepts/agents#yaml-configuration-recommended
    # Tasks: https://docs.crewai.com/concepts/tasks#yaml-configuration-recommended
    agents_config = 'config/agents.yaml'
    tasks_config = 'config/tasks.yaml'

    @before_kickoff
    def before_kickoff_function(self, inputs):
        print(f"Before kickoff function with inputs: {inputs}")
        return inputs # You can return the inputs or modify them as needed

    @after_kickoff
    def after_kickoff_function(self, result):
        print(f"After kickoff function with result: {result}")
        return result # You can return the result or modify it as needed

    # If you would like to add tools to your agents, you can learn more about it here:
    # https://docs.crewai.com/concepts/agents#agent-tools
    @agent
    def researcher(self) -> Agent:
        return Agent(
            config=self.agents_config['researcher'],
            tools= [ScrapeWebsiteTool()],
            verbose=True
        )
    
    @agent
    def career_expert(self) -> Agent:
        return Agent(
            config=self.agents_config['career_expert'],
            verbose=True
        )

    # To learn more about structured task outputs,
    # task dependencies, and task callbacks, check out the documentation:
    # https://docs.crewai.com/concepts/tasks#overview-of-a-task

    @task
    def job_opening_task(self) -> Task:
        return Task(
            config=self.tasks_config['job_opening_task'],
            output_json=JobPostingModel,

        )
    
    @task
    def job_analysis_task(self) -> Task:
        return Task(
            config=self.tasks_config['job_analysis_task'],
            output_file='report.md'

        )

    @crew
    def crew(self) -> Crew:
        """Creates the JobHunting crew"""
        # To learn how to add knowledge sources to your crew, check out the documentation:
        # https://docs.crewai.com/concepts/knowledge#what-is-knowledge

        return Crew(
            agents=self.agents, # Automatically created by the @agent decorator
            tasks=self.tasks, # Automatically created by the @task decorator
            process=Process.sequential,
            verbose=True,
            # process=Process.hierarchical, # In case you wanna use that instead https://docs.crewai.com/how-to/Hierarchical/
        )
