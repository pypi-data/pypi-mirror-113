import numpy as np
from gibson2.utils.utils import rotate_vector_3d, cartesian_to_polar
from gibson2.envs.locomotor_env import NavigateRandomEnv


class NavigateRandomEnv2(NavigateRandomEnv):
    """
    Follows the DD-PPO paper and use [d, cos(theta), sin(theta)] as GPS + compass
    """

    def load_task_setup(self):
        super().load_task_setup()
        self.additional_states_dim = 5

    def get_additional_states(self):
        """
        Goal format: [d, cos(theta), sin(theta)]
        """
        additional_states = self.global_to_local(self.target_pos)[:2]
        assert self.goal_format == "polar"
        rho, phi = cartesian_to_polar(additional_states[0], additional_states[1])
        additional_states = np.array([rho, np.cos(phi), np.sin(phi)], dtype=np.float32)

        # linear velocity along the x-axis
        linear_velocity = rotate_vector_3d(
            self.robots[0].get_linear_velocity(), *self.robots[0].get_rpy()
        )[0]
        # angular velocity along the z-axis
        angular_velocity = rotate_vector_3d(
            self.robots[0].get_angular_velocity(), *self.robots[0].get_rpy()
        )[2]
        additional_states = np.append(
            additional_states, [linear_velocity, angular_velocity]
        )

        if self.config["task"] == "reaching":
            end_effector_pos_local = self.global_to_local(
                self.robots[0].get_end_effector_position()
            )
            additional_states = np.append(additional_states, end_effector_pos_local)

        assert additional_states.shape[0] == self.additional_states_dim, (
            f"additional states dimension mismatch {additional_states.shape[0]} "
            f"v.s. {self.additional_states_dim}"
        )
        return additional_states
