import time

from clgridworld.grid_world_action import GridWorldAction
from clgridworld.grid_world_builder import GridWorldBuilder, InitialStateParams
from gym import wrappers, logger


class RandomAgent(object):
    """The world's simplest agent!"""
    def __init__(self, action_space):
        self.action_space = action_space

    def act(self, observation, reward, done):
        return self.action_space.sample()


if __name__ == '__main__':

    # target task spec as defined in Source Task Sequencing,,, Narvekar et al 2017
    params = InitialStateParams(shape=(10, 10), player=(1, 4), key=(7, 5), lock=(1, 1), pit_start=(4, 2), pit_end=(4, 7))

    # You can set the level to logger.DEBUG or logger.WARN if you
    # want to change the amount of output.
    logger.set_level(logger.INFO)

    env = GridWorldBuilder.create(params)

    # You provide the directory to write to (can be an existing
    # directory, including one with existing data -- all monitor files
    # will be namespaced). You can also dump to a tempdir if you'd
    # like: tempfile.mkdtemp().
    outdir = '/tmp/random-agent-results'
    env = wrappers.Monitor(env, directory=outdir, force=True)
    env.seed(0)
    agent = RandomAgent(env.action_space)

    episode_count = 10
    reward = 0
    done = False

    for i in range(episode_count):
        ob = env.reset()
        env.render()
        print("\n")
        step_count = 0
        accum_reward = 0
        while True:
            action = agent.act(ob, reward, done)
            ob, reward, done, _ = env.step(action)
            step_count += 1
            accum_reward += reward

            env.render()
            print("episode: " + str(i) + "." + str(step_count))
            print("action: " + GridWorldAction.NAMES[action])
            print("reward: " + str(reward))
            print("accum reward: " + str(accum_reward))
            print("\n")
            # time.sleep(0.5)

            if done:
                break

    # Close the env and write monitor result info to disk
    env.close()