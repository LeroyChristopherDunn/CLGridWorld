import time

from clgridworld.grid_world_action import GridWorldAction
from clgridworld.grid_world_builder import GridWorldBuilder, InitialStateParams
from gym import wrappers, logger


class RandomAgent(object):
    """The world's simplest agent!"""
    def __init__(self, action_space):
        self.action_space = action_space

    def act(self, observation):
        return self.action_space.sample()


if __name__ == '__main__':

    # You can set the level to logger.DEBUG or logger.WARN if you
    # want to change the amount of output.
    logger.set_level(logger.INFO)

    params = InitialStateParams(shape=(10, 10), player=(1, 4), lock=(9, 1))
    env = GridWorldBuilder.create(params)
    seed = 0
    env.seed(seed)
    agent = RandomAgent(env.action_space)

    print("Generated environment: ")
    env.render()
    print("")

    num_episodes = 100
    max_steps_per_episode = 5000
    episodic_rewards = []

    for i in range(num_episodes):

        reward = 0
        done = False
        curr_state = env.reset()
        step_count = 0
        accum_reward = 0

        while True:

            prev_state = curr_state
            action = agent.act(curr_state)
            curr_state, reward, done, _ = env.step(action)

            step_count += 1
            accum_reward += reward

            # env.render()
            # print("episode: " + str(i) + "." + str(step_count))
            # print("action: " + GridWorldAction.NAMES[action])
            # print("reward: " + str(reward))
            # print("accum reward: " + str(accum_reward))
            # print("\n")
            # time.sleep(0.5)

            if done or step_count >= max_steps_per_episode:
                break

        episodic_rewards.append(accum_reward)
        print("episode {} reward: {}".format(i, accum_reward))

    env.close()