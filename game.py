import muzero_model
from utils import *


class Game:
    def __init__(self, settings, action_space):
        self.observation_history = []
        self.actions_history = []
        self.rewards_history = []
        self.child_visits = []
        self.root_values = []
        self.discount = settings.discount
        self.action_space = action_space

    def store_MTCS_stat(self, root):
        sum_visits = sum(child.visit_count for child in root.children.values())
        self.child_visits.append([root.children[a].visit_count / sum_visits if a in root.children else 0 for a in range(self.action_space)])
        self.root_values.append(root.value())

    def get_stacked_observations(self, index, num_stacked_observations):
        index = index % len(self.observation_history)
        stacked_obs = self.observation_history[index].copy()
        for past_obs_idx in reversed(range(index - num_stacked_observations, index)):
            if 0 <= past_obs_idx:
                previous_obs = np.concatenate((self.observation_history[past_obs_idx], [np.ones_like(stacked_obs[0]) * self.actions_history[past_obs_idx + 1]]))
            else:
                # TODO: Duplicate 'index' frame
                previous_obs = np.concatenate((np.zeros_like(self.observation_history[index]), [np.zeros_like(stacked_obs[0])]))

            stacked_obs = np.concatenate((stacked_obs, previous_obs))

        return stacked_obs