from oneflow.experimental.optim.lr_scheduler import LambdaLR
import math

class WarmupLinearSchedule(LambdaLR):
    """ Linear warmup and then linear decay.
        Linearly increases learning rate from 0 to 1 over `warmup_steps` training steps.
        Linearly decreases learning rate from 1. to 0. over remaining `t_total - warmup_steps` steps.
    """
    def __init__(self, optimizer, warmup_steps, t_total, last_step=-1):
        self.warmup_steps = warmup_steps
        self.t_total = t_total
        self.optimizer = optimizer
        super(WarmupLinearSchedule, self).__init__(optimizer, self.lr_lambda, last_step=last_step)

    def lr_lambda(self, step):
        if step < self.warmup_steps:
            return float(step) / float(max(1, self.warmup_steps))
        return max(0.0, float(self.t_total - step) / float(max(1.0, self.t_total - self.warmup_steps)))
    
    def get_step_values(self):
        return self.optimizer.param_groups[0]['lr']