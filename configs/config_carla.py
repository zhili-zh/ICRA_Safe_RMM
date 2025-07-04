import argparse


def get_config():
    """
    The configuration parser for common hyperparameters of all environment. 
    Please reach each `scripts/train/<env>_runner.py` file to find private hyperparameters
    only used in <env>.

    Prepare parameters:
        --algorithm_name <algorithm_name>
            specifiy the algorithm, including `["rmappo", "mappo", "rmappg", "mappg", "trpo"]`
        --experiment_name <str>
            an identifier to distinguish different experiment.
        --seed <int>
            set seed for numpy and torch 
        --cuda
            by default True, will use GPU to train; or else will use CPU; 
        --cuda_deterministic
            by default, make sure random seed effective. if set, bypass such function.
        --n_training_threads <int>
            number of training threads working in parallel. by default 1
        --n_rollout_threads <int>
            number of parallel envs for training rollout. by default 32
        --n_eval_rollout_threads <int>
            number of parallel envs for evaluating rollout. by default 1
        --n_render_rollout_threads <int>
            number of parallel envs for rendering, could only be set as 1 for some environments.
        --num_env_steps <int>
            number of env steps to train (default: 10e6)
        --user_name <str>
            [for wandb usage], to specify user's name for simply collecting training data.
        --use_wandb
            [for wandb usage], by default True, will log date to wandb server. or else will use tensorboard to log data.
    
    Env parameters:
        --env_name <str>
            specify the name of environment
        --use_obs_instead_of_state
            [only for some env] by default False, will use global state; or else will use concatenated local obs.
    
    Replay Buffer parameters:
        --episode_length <int>
            the max length of episode in the buffer. 
    
    Network parameters:
        --share_policy
            by default True, all agents will share the same network; set to make training agents use different policies. 
        --use_centralized_V
            by default True, use centralized training mode; or else will decentralized training mode.
        --stacked_frames <int>
            Number of input frames which should be stack together.
        --hidden_size <int>
            Dimension of hidden layers for actor/critic networks
        --layer_N <int>
            Number of layers for actor/critic networks
        --use_ReLU
            by default True, will use ReLU. or else will use Tanh.
        --use_popart
            by default True, use PopArt to normalize rewards. 
        --use_valuenorm
            by default True, use running mean and std to normalize rewards. 
        --use_feature_normalization
            by default True, apply layernorm to normalize inputs. 
        --use_orthogonal
            by default True, use Orthogonal initialization for weights and 0 initialization for biases. or else, will use xavier uniform inilialization.
        --gain
            by default 0.01, use the gain # of last action layer
        --use_naive_recurrent_policy
            by default False, use the whole trajectory to calculate hidden states.
        --use_recurrent_policy
            by default, use Recurrent Policy. If set, do not use.
        --recurrent_N <int>
            The number of recurrent layers ( default 1).
        --data_chunk_length <int>
            Time length of chunks used to train a recurrent_policy, default 10.
    
    Optimizer parameters:
        --lr <float>
            learning rate parameter,  (default: 5e-4, fixed).
        --critic_lr <float>
            learning rate of critic  (default: 5e-4, fixed)
        --opti_eps <float>
            RMSprop optimizer epsilon (default: 1e-5)
        --weight_decay <float>
            coefficience of weight decay (default: 0)
    
    PPO parameters:
        --ppo_epoch <int>
            number of ppo epochs (default: 15)
        --use_clipped_value_loss 
            by default, clip loss value. If set, do not clip loss value.
        --clip_param <float>
            ppo clip parameter (default: 0.2)
        --num_mini_batch <int>
            number of batches for ppo (default: 1)
        --entropy_coef <float>
            entropy term coefficient (default: 0.01)
        --use_max_grad_norm 
            by default, use max norm of gradients. If set, do not use.
        --max_grad_norm <float>
            max norm of gradients (default: 0.5)
        --use_gae
            by default, use generalized advantage estimation. If set, do not use gae.
        --gamma <float>
            discount factor for rewards (default: 0.99)
        --gae_lambda <float>
            gae lambda parameter (default: 0.95)
        --use_proper_time_limits
            by default, the return value does consider limits of time. If set, compute returns with considering time limits factor.
        --use_huber_loss
            by default, use huber loss. If set, do not use huber loss.
        --use_value_active_masks
            by default True, whether to mask useless data in value loss.  
        --huber_delta <float>
            coefficient of huber loss.  
    
    PPG parameters:
        --aux_epoch <int>
            number of auxiliary epochs. (default: 4)
        --clone_coef <float>
            clone term coefficient (default: 0.01)
    
    Run parameters：
        --use_linear_lr_decay
            by default, do not apply linear decay to learning rate. If set, use a linear schedule on the learning rate
    
    Save & Log parameters:
        --save_interval <int>
            time duration between contiunous twice models saving.
        --log_interval <int>
            time duration between contiunous twice log printing.
    
    Eval parameters:
        --use_eval
            by default, do not start evaluation. If set`, start evaluation alongside with training.
        --eval_interval <int>
            time duration between contiunous twice evaluation progress.
        --eval_episodes <int>
            number of episodes of a single evaluation.
    
    Render parameters:
        --save_gifs
            by default, do not save render video. If set, save video.
        --use_render
            by default, do not render the env during training. If set, start render. Note: something, the environment has internal render process which is not controlled by this hyperparam.
        --render_episodes <int>
            the number of episodes to render a given env
        --ifi <float>
            the play interval of each rendered image in saved video.
    
    Pretrained parameters:
        --model_dir <str>
            by default None. set the path to pretrained model.
    """
    #parser = argparse.ArgumentParser(description='onpolicy', formatter_class=argparse.RawDescriptionHelpFormatter)
    parser = argparse.ArgumentParser("Reinforcement Learning experiments for multiagent environments")

    # prepare parameters
    parser.add_argument("--algorithm_name", type=str, default='mappo', choices=["rppo", "wmappo", "rmappo", "mappo", "maa2c"])
    parser.add_argument("--experiment_name", type=str, default="train_carla", help="an identifier to distinguish different experiment.")
    parser.add_argument("--seed", type=int, default=912, help="Random seed for numpy/torch")
    parser.add_argument("--cuda", action='store_false', default=True, help="by default True, will use GPU to train; or else will use CPU;")
    parser.add_argument("--cuda_deterministic", action='store_false', default=True, help="by default, make sure random seed effective. if set, bypass such function.")
    parser.add_argument("--n_training_threads", type=int, default=1, help="Number of torch threads for training")
    parser.add_argument("--n_rollout_threads", type=int, default=1, help="Number of parallel envs for training rollouts")
    parser.add_argument("--n_eval_rollout_threads", type=int, default=1, help="Number of parallel envs for evaluating rollouts")
    #parser.add_argument("--n_render_rollout_threads", type=int, default=1,
    #                    help="Number of parallel envs for rendering rollouts")
    parser.add_argument("--num_env_steps", type=int, default=100000, help='Number of environment steps to train (default: 10e6)')
    parser.add_argument("--user_name", type=str, default='zzl',help="[for wandb usage], to specify user's name for simply collecting training data.")
    parser.add_argument("--use_wandb", action='store_true', default=False, help="[for wandb usage], by default True, will log date to wandb server. or else will use tensorboard to log data.")

    # env parameters
    parser.add_argument("--env_name", type=str, default='CARLA', help="specify the name of environment")
    parser.add_argument("--use_obs_instead_of_state", action='store_true', default=False, help="Whether to use global state or concatenated obs")

    # replay buffer parameters
    parser.add_argument("--episode_length", type=int,
                        default=300, help="Max length for any episode")

    # network parameters
    parser.add_argument("--share_policy", action='store_true',
                        default=False, help='Whether agent share the same policy')
    parser.add_argument("--use_centralized_V", action='store_true',
                        default=False, help="Whether to use centralized V function")
    parser.add_argument("--stacked_frames", type=int, default=1,
                        help="Dimension of hidden layers for actor/critic networks")
    parser.add_argument("--use_stacked_frames", action='store_true',
                        default=False, help="Whether to use stacked_frames")
    parser.add_argument("--hidden_size", type=int, default=32,
                        help="Dimension of hidden layers for actor/critic networks") 
    parser.add_argument("--layer_N", type=int, default=1,
                        help="Number of layers for actor/critic networks")
    parser.add_argument("--use_ReLU", action='store_false',
                        default=True, help="Whether to use ReLU")
    parser.add_argument("--use_popart", action='store_true', default=False, help="by default False, use PopArt to normalize rewards.")
    parser.add_argument("--use_valuenorm", action='store_false', default=True, help="by default True, use running mean and std to normalize rewards.")
    parser.add_argument("--use_feature_normalization", action='store_true', default=False, help="Whether to apply layernorm to the inputs")
    parser.add_argument("--use_orthogonal", action='store_false', default=True, help="Whether to use Orthogonal initialization for weights and 0 initialization for biases")
    parser.add_argument("--gain", type=float, default=0.01,
                        help="The gain # of last action layer")

    # recurrent parameters
    parser.add_argument("--use_naive_recurrent_policy", action='store_true',
                        default=False, help='Whether to use a naive recurrent policy')
    parser.add_argument("--use_recurrent_policy", action='store_true',
                        default=False, help='use a recurrent policy')
    parser.add_argument("--recurrent_N", type=int, default=1, help="The number of recurrent layers.")
    parser.add_argument("--data_chunk_length", type=int, default=20,
                        help="Time length of chunks used to train a recurrent_policy")

    # transformer or GNN
    # parser.add_argument("--use_transformer", action='store_true', default=False, help='use transformer in actor and critic')
    # parser.add_argument("--use_gnn", action='store_true', default=False, help='use gnn in actor and critic')
    # parser.add_argument('--gnn', default='gcn', type=str, choices=['gat', 'gcn', 'n2v'], help='what gnn to use')
    # parser.add_argument('--gnn_pooling', default='att', type=str, choices=['mean', 'max', 'att', 'none'], help='what pooling strategy')
    # parser.add_argument('--walk_length', default=3, type=int, help='walk length in node2vec')

    # optimizer parameters
    parser.add_argument("--lr", type=float, default=5e-4,
                        help='learning rate (default: 5e-4)')
    parser.add_argument("--critic_lr", type=float, default=5e-4,
                        help='critic learning rate (default: 5e-4)')
    parser.add_argument("--opti_eps", type=float, default=1e-5,
                        help='RMSprop optimizer epsilon (default: 1e-5)')
    parser.add_argument("--weight_decay", type=float, default=0)

    # ppo parameters
    parser.add_argument("--ppo_epoch", type=int, default=15,
                        help='number of ppo epochs (default: 15)')
    parser.add_argument("--use_clipped_value_loss",
                        action='store_false', default=True, help="by default, clip loss value. If set, do not clip loss value.")
    parser.add_argument("--clip_param", type=float, default=0.1,
                        help='ppo clip parameter (default: 0.1)')
    parser.add_argument("--num_mini_batch", type=int, default=1,
                        help='number of batches for ppo (default: 1)')
    parser.add_argument("--entropy_coef", type=float, default=0.01,
                        help='entropy term coefficient (default: 0.01)')
    parser.add_argument("--value_loss_coef", type=float,
                        default=1, help='value loss coefficient (default: 0.5)')
    parser.add_argument("--use_max_grad_norm",
                        action='store_false', default=True, help="by default, use max norm of gradients. If set, do not use.")
    parser.add_argument("--max_grad_norm", type=float, default=10.0,
                        help='max norm of gradients (default: 0.5)')
    parser.add_argument("--use_gae", action='store_false',
                        default=True, help='use generalized advantage estimation')
    parser.add_argument("--gamma", type=float, default=0.99,
                        help='discount factor for rewards (default: 0.99)')
    parser.add_argument("--gae_lambda", type=float, default=0.95,
                        help='gae lambda parameter (default: 0.95)')
    parser.add_argument("--use_proper_time_limits", action='store_true',
                        default=False, help='compute returns taking into account time limits')
    parser.add_argument("--use_huber_loss", action='store_false', default=True, help="by default, use huber loss. If set, do not use huber loss.")
    parser.add_argument("--use_value_active_masks",
                        action='store_false', default=True, help="by default True, whether to mask useless data in value loss.")
    parser.add_argument("--use_policy_active_masks",
                        action='store_false', default=True, help="by default True, whether to mask useless data in policy loss.")
    parser.add_argument("--huber_delta", type=float, default=10.0, help=" coefficience of huber loss.")

    # wocar parameters
    parser.add_argument("--wqw", type=float, default=0.05, help='worst q weight in loss function')
    parser.add_argument("--weight_schedule", type=str, default='exp', help='worst q weight schedule strategy during training')
    parser.add_argument("--robust_reg", type=float, default=0.2, help='regularizer weight in actor loss function')
    parser.add_argument("--wq_loss_coef", type=float, default=1.0, help='worst q loss coefficient (default: 1.0)')
    parser.add_argument("--eps", type=float, default=5., help='eps for robustness')
    parser.add_argument("--eps_start", type=float, default=0.2, help='starting episode implementing eps')

    # run parameters
    parser.add_argument("--use_linear_lr_decay", action='store_true',
                        default=False, help='use a linear schedule on the learning rate')
    parser.add_argument("--random_mapping_agents", action='store_true',
                        default=False, help='randomize the allocation of policy to cav agents')
    
    # save parameters
    parser.add_argument("--save_interval", type=int, default=1, help="time duration between contiunous twice models saving.")

    # log parameters
    parser.add_argument("--log_interval", type=int, default=1, help="time duration between contiunous twice log printing.")

    # eval parameters
    parser.add_argument("--use_eval", action='store_true', default=False, help="by default, do not start evaluation. If set`, start evaluation alongside with training.")
    parser.add_argument("--eval_interval", type=int, default=25, help="time duration between contiunous twice evaluation progress.")
    parser.add_argument("--eval_episodes", type=int, default=32, help="number of episodes of a single evaluation.")

    # render parameters
    #parser.add_argument("--save_gifs", action='store_true', default=False, help="by default, do not save render video. If set, save video.")
    parser.add_argument("--use_render", action='store_true', default=False, help="by default, do not render the env during training. If set, start render. Note: something, the environment has internal render process which is not controlled by this hyperparam.")
    #parser.add_argument("--render_episodes", type=int, default=5, help="the number of episodes to render a given env")
    #parser.add_argument("--ifi", type=float, default=0.1, help="the play interval of each rendered image in saved video.")

    # pretrained parameters
    parser.add_argument("--model_dir", type=str, default=None, help="by default None. set the path to pretrained model.")

    # CARLA-related parameters
    parser.add_argument('-v', '--verbose', action='store_true', dest='debug', help='print debug information')
    parser.add_argument('--host', metavar='H', default="127.0.0.1", help='IP of the host server (default: "localhost")')
    parser.add_argument('-p', '--port', metavar='P', default=2000, type=int, help='TCP port to listen to (default: 2000)')
    parser.add_argument('-t', '--timestep', metavar='DT', default=0.05, type=float, help='simulation timestep length in seconds (default: 0.05)')
    parser.add_argument('-m', '--map', default='Town06', type=str, help='map name (default: Town06)')
    parser.add_argument('-c', '--cars', metavar='C', default=5, type=int, help='number of vehicles')
    parser.add_argument('--spec_view', default='side_up', choices=['front_up', 'side_up', 'birdeye', 'none'], type=str, help='Scenario where the hazard takes place, either cross or merge')
    parser.add_argument('--num_agents', default=1, type=int, help='number of connected autonomous vehicles')
    parser.add_argument('--safety_step', default=40, type=int, help='number of steps looking forward in safety checking')
    parser.add_argument('--disable_lane_chg', default=False, action='store_true', help='let the safety checking disable the lane-change actions')
    parser.add_argument('--disable_CBF', default=False, action='store_true', help='disable the CBF safety checking')
    parser.add_argument('--brief_state', default=False, action='store_true', help='shorten the state space for each agent from 16 to 7')
    parser.add_argument('--normal_behave', default=False, action='store_true', help='the hazard vehicle will drive safely')
    parser.add_argument('--remove_CBFA', default=False, action='store_true', help='if true, disable the acceleration sharing in CBF')
    parser.add_argument('--e_type', default=None, type=str, choices=['noise', 'miss', 'l_attack', 'f_attack', 'critic', 'tgt_v', 'tgt_t'], help='type of error for testing robustness')
    parser.add_argument('--attack', default='none', type=str, choices=['none', 'critic'], help='type of attack')
    parser.add_argument('--cbf_robustness', default=2.0, type=float, help='robustness coefficient in robust CBF')
    parser.add_argument('--enco', default=None, type=str, choices=['lane_change', 'speed', 'none'], help='whether encourage certain actions')
    parser.add_argument('--encourage_r', default=0.0, type=float, help='the reward encouraging agents to choose certain actions')
    parser.add_argument('--avg_coef', default=1.0, type=float, help='the reward encouraging agents to choose certain actions')
    parser.add_argument('--apply_safe_reward', default=False, action='store_true', help='Whether to apply safety rewards from MPC-CBF controller for MARL')
    parser.add_argument('--centralized', default=False, action='store_true', help='Whether apply centralized training for MARL')
    parser.add_argument('--deterministic', default=False, action='store_true', help='Whether use deterministic policy, default is stochastic policy')
    parser.add_argument('--no_render', default=False, action='store_true', help='prevent Unreal Engine from rendering the scene')
    parser.add_argument('--test_only', default=False, action='store_true', help='Option to do testing only (no training)')
    parser.add_argument('--episodes', type=int, default=500, help='total number of simulation episodes (default: 100)')
    parser.add_argument('--flow_reward_coef', type=float, default=1., help='multiplicated coefficient to flow reward (speed of CAVs)')
    parser.add_argument('--discretize',  type=int, default=0, choices=[0,3,4,5], help='Number of discretized range for throttle and brake')
    parser.add_argument('--scene_n',  type=int, default=0, choices=[0,1,2,3], help='Number of config to load in specific scenario')
    parser.add_argument('--scenario_name',  type=str,  default='highway',  choices=['highway', 'crossing', 'both'], help="Which scenario to run on")
    parser.add_argument('--sabbir_control', default=False, action='store_true', help='Option to hardcode the UCV behavior in both highway and crossing')
    parser.add_argument('--rule_based_r', default=False, action='store_true', help='Option to include the rule-based reward when training')
    parser.add_argument('--run_rule_based_benchmark', default=False, action='store_true', help='running the rule-based method benchmark')
    parser.add_argument('--middle3', default=False, action='store_true', help='allowing only middle 3 lanes in highway')
    parser.add_argument("--ucv_fs_step", type=int, default=10, help="unconnected vehicle force_straight_step")
    parser.add_argument("--cav_fs_step", type=int, default=0, help="CAV force_straight_step")
    parser.add_argument("--temporal_length", type=int, default=1, choices=[1, 5, 10, 20], help="CAV force_straight_step")
    # parser.add_argument("--threshold", type=float, default=0., help="CAV force_straight_step")

    return parser
