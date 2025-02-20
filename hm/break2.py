import snake2 as snake
import numpy as np
import tensorflow as tf
from tensorflow import keras
from keras import layers
from sys import argv
import time

stime=time.time()

# Configuration paramaters for the whole setup
seed = 42
gamma = 0.99  # init at .99 try reducing Discount factor for past rewards
epsilon = 1.0  # Epsilon greedy parameter
epsilon_min = 0.1  # Minimum epsilon greedy parameter
epsilon_max = 1.0  # Maximum epsilon greedy parameter
epsilon_interval = (epsilon_max - epsilon_min)  # Rate at which to reduce chance of random action being taken
batch_size = 32  # Size of batch taken from replay buffer
max_steps_per_episode = 15000
rfc=0
ph=0
fpos = [(0,0),(0,snake.size-1),(snake.size-1,0),(snake.size-1,snake.size-1),(snake.size//2,snake.size//2),(0,0),(0,snake.size-1),(snake.size-1,0),(snake.size-1,snake.size-1)]
# Use the Baseline Atari environment because of Deepmind helper functions
env = snake.snake_board(fpos=fpos)
# Warp the frames, grey scale, stake four frame and scale to smaller ratio

num_actions = 4

def create_q_model():
    # Network defined by the Deepmind paper
    inputs = layers.Input(shape=(snake.size,snake.size,2,))
    # Convolutions on the frames on the screen
    layer1 = layers.Conv2D(8, 8, strides=4, activation="relu")(inputs)
    layer2 = layers.Conv2D(16, 4, strides=2, activation="relu")(layer1)
    layer3 = layers.Conv2D(8, 3, strides=1, activation="relu")(layer2)

    layer4 = layers.Flatten()(layer3)

    layer5 = layers.Dense(256, activation="relu")(layer4)
    action = layers.Dense(num_actions, activation="linear")(layer5)

    return keras.Model(inputs=inputs, outputs=action)


# The first model makes the predictions for Q-values which are used to
# make a action.
model = create_q_model()
# Build a target model for the prediction of future rewards.
# The weights of a target model get updated every 10000 steps thus when the
# loss between the Q-values is calculated the target Q-value is stable.
model_target = create_q_model()

optimizer = keras.optimizers.Adam(learning_rate=0.00025, clipnorm=1.0)


# Experience replay buffers
action_history = []
state_history = []
state_next_history = []
rewards_history = []
done_history = []
episode_reward_history = []
deaths = 0
running_reward = 0
episode_count = 0
frame_count = 0
# Number of frames to take random action and observe output
epsilon_random_frames = 5000
# Number of frames for exploration
epsilon_greedy_frames = 15000
# Maximum replay length
# Note: The Deepmind paper suggests 1000000 however this causes memory issues
max_memory_length = 10000
# Train the model after 4 actions
update_after_actions = 4
# How often to update the target network
update_target_network = 1000
# Using huber loss for stability
loss_function = keras.losses.Huber()

if not len(argv)>1:
    try:
        model.load_weights('./mod1hm/')
        model_target.load_weights('./mod2hm/')
        epsilon_random_frames/=10
        print("\nLoaded Models Succesfully\n")

    except:
        print('no save found')

while True:  # Run until solved
    m = fpos.copy()
    state = np.array(env.reset(m))
    episode_reward = 0
    for timestep in range(1, max_steps_per_episode):
        # env.render(); Adding this line would show the attempts
        # of the agent in a pop up window.
        if frame_count%10000==0:
            seconds = time.time()-stime
            minutes, seconds = divmod(seconds, 60)
            hours, minutes = divmod(minutes, 60)
            print("saving model...\nCurrent Run Time:%d:%02d:%02d" % (hours, minutes, seconds))
            model.save_weights("./mod1hm/")
            model_target.save_weights("./mod2hm/")
        frame_count += 1
        if frame_count < epsilon_random_frames or epsilon > np.random.rand(1)[0]:
            if epsilon>1:
                epsilon-=0.3
            action = np.random.choice(num_actions)
            rfc+=1
        else:
            # Predict action Q-values
            # From environment state
            state_tensor = tf.convert_to_tensor(state)
            state_tensor = tf.expand_dims(state_tensor, 0)
            action_probs = model(state_tensor, training=False)
            # Take best action
            action = tf.argmax(action_probs[0]).numpy()

        # Decay probability of taking random action
        epsilon -= epsilon_interval / epsilon_greedy_frames
        epsilon = max(epsilon, epsilon_min)
        # Apply the sampled action in our environment
        state_next, reward, done, snake_size = env.step(action)
        state_next = np.array(state_next)
        episode_reward += reward
        # Save actions and states in replay buffer
        action_history.append(action)
        state_history.append(state)
        state_next_history.append(state_next)
        done_history.append(done)
        rewards_history.append(reward)
        state = state_next
        # Update every fourth frame and once batch size is over 32
        if frame_count % update_after_actions == 0 and len(done_history) > batch_size:

            # Get indices of samples for replay buffers
            indices = np.random.choice(range(len(done_history)), size=batch_size)

            # Using list comprehension to sample from replay buffer
            state_sample = np.array([state_history[i] for i in indices])
            state_next_sample = np.array([state_next_history[i] for i in indices])
            rewards_sample = [rewards_history[i] for i in indices]
            action_sample = [action_history[i] for i in indices]
            done_sample = tf.convert_to_tensor(
                [float(done_history[i]) for i in indices]
            )

            # Build the updated Q-values for the sampled future states
            # Use the target model for stability
            future_rewards = model_target.predict(state_next_sample,verbose=0)
            # Q value = reward + discount factor * expected future reward
            updated_q_values = rewards_sample + gamma * tf.reduce_max(
                future_rewards, axis=1)

            # If final frame set the last value to -1
            updated_q_values = updated_q_values * (1 - done_sample) - done_sample

            # Create a mask so we only calculate loss on the updated Q-values
            masks = tf.one_hot(action_sample, num_actions)

            with tf.GradientTape() as tape:
                # Train the model on the states and updated Q-values
                q_values = model(state_sample)

                # Apply the masks to the Q-values to get the Q-value for action taken
                q_action = tf.reduce_sum(tf.multiply(q_values, masks), axis=1)
                # Calculate loss between new Q-value and old Q-value
                loss = loss_function(updated_q_values, q_action)

            # Backpropagation
            grads = tape.gradient(loss, model.trainable_variables)
            optimizer.apply_gradients(zip(grads, model.trainable_variables))

        if frame_count % update_target_network == 0:
            # update the the target network with new weights
            model_target.set_weights(model.get_weights())
            # Log details
            mrh_ = np.mean(rewards_history)
            template = "avg rew: {0:.2f} at episode {1}, frame count {2},Num rand frame: {3}, reward: {4:.3f},snake size:{5},epsilon:{6:0.4f},deaths: {7}"
            print(template.format(mrh_, episode_count, frame_count,rfc,reward,snake_size,epsilon,deaths))
            if mrh_-ph <=0.01 and reward<(0.5*snake.size):
                epsilon+=0.2
                epsilon=min(epsilon_max,epsilon)
            ph = mrh_
        # Limit the state and reward history
        if len(rewards_history) > max_memory_length:
            del rewards_history[:1]
            del state_history[:1]
            del state_next_history[:1]
            del action_history[:1]
            del done_history[:1]
        if done==True:
            deaths+=1
            break
    # Update running reward to check condition for solving
    episode_reward_history.append(episode_reward)
    if len(episode_reward_history) > 100:
        del episode_reward_history[:1]
    running_reward = np.mean(episode_reward_history)

    episode_count += 1
    if snake_size>=len(fpos)-1 if fpos!=None else 5:  # Condition to consider the task solved
        model.save_weights("./mod1hm/")
        model_target.save_weights("./mod2hm/")
        print("Solved at episode {}!".format(episode_count))
        break