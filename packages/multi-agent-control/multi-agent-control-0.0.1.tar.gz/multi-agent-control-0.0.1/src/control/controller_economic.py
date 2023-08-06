from collections import defaultdict

import numpy as np

class EconomicControl:

    def __init__(self, env, agents, tasks):
        self.env = env
        self.agents = agents
        self.tasks = tasks
        self.given_tasks = defaultdict(list)

    def get_joint_action(self, observation):
        joint_action = {
            agent_name: self.agents[agent_name].get_action(observation[agent_name])
            for agent_name in self.agents.keys()     
        }
        return joint_action

    def run(self, max_episode_lenth=np.inf):
        """Runs the economic control on the env given in init

        Args:
            max_episode_lenth (int, optional): number of steps. Defaults to np.inf.
        """
        observation = self.env.reset()
        # We need to give the agents their position so they will know to bid
        for agent_name in self.agents.keys():
            self.agents[agent_name].reset(observation[agent_name])
        
        # Auction the tasks:
        self._auction_all_tasks()
        i = 1
        done = {'temp_agent': False}
        while(not all(value == True for value in done.values()) 
                and i < max_episode_lenth):
            print(f"Step {i}:")
            i += 1
            actions = self.get_joint_action(observation)
            observation, reward, done, info = self.env.step(actions)
            self.env.render()
        print(f"Finished")

    def _auction_all_tasks(self):
        """Auctions all the tasks given at init
        """
        non_busy_agents = list(self.agents.keys())
        for task in self.tasks:
            agent_chosen = self._auction_task(task, non_busy_agents)
            del(non_busy_agents[non_busy_agents.index(agent_chosen)])

    def _auction_task(self, task, agents):
        """Auction out tasks, and gives it to the agent that bids lowest.
        We remember the task so we can reward the agent when it is complete.
        """
        bids = {agent_name: self.agents[agent_name].get_bid(task) for agent_name in agents}
        agent_name = min(bids.keys(), key=(lambda k: bids[k]))
        self.agents[agent_name].set_task(task)
        self.given_tasks[agent_name].append(task)
        return agent_name