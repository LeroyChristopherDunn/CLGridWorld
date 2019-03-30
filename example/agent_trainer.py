import gym
import numpy as np

from example.agents.agent import Agent
import matplotlib.pyplot as plt


class AgentTrainer:

    def __init__(self, env: gym.Env, agent: Agent):
        self.env = env
        self.agent = agent

    def train(self, seed=0, num_episodes=5000, max_steps_per_episode=10000, episode_log_interval=100):

        env = self.env
        agent = self.agent

        env.seed(seed)

        print("Environment initial state: ")
        env.render()
        print("")

        episodic_rewards = []

        for i in range(num_episodes):

            curr_state = env.reset()
            step_count = 0
            accum_reward = 0

            while True:

                prev_state = curr_state
                action = agent.get_action(curr_state)
                curr_state, reward, done, _ = env.step(action)
                agent.update(prev_state, action, curr_state, reward)

                step_count += 1
                accum_reward += reward

                ## uncomment the below lines to render the environment to terminal
                # env.render()
                # print("episode: " + str(i) + "." + str(step_count))
                # print("action: " + GridWorldAction.NAMES[action])
                # print("reward: " + str(reward))
                # print("accum reward: " + str(accum_reward))
                # print("epsilon: " + str(agent.epsilon))
                # print("\n")
                # time.sleep(0.5)

                if done or step_count >= max_steps_per_episode:
                    break

            agent.inc_episode()

            episodic_rewards.append(accum_reward)
            if i % episode_log_interval == 0:
                avg_reward = np.average(episodic_rewards[-episode_log_interval:])
                print("episode {} avg reward: {}".format(i, avg_reward))

        plt.plot(episodic_rewards)
        plt.ylabel('Episodic Reward')
        plt.xlabel('Episode')
        plt.show()

        env.close()
