
# 登录界面
# from .login_main import Login_Main
from .login_window import LogMain
# 选择界面
from .center_menu_main import Center_Menu_Main
from .lessons_select_main import Lessons_Select_Main
from .std_train_select_main import Std_Train_Select_Main

# 反应训练界面
from .reaction_train_main import Reaction_Train_Main

from .Grade_main import Grade_reaction, Grade_std


from .std_train_select_main import Std_Train_Select_Main
from .setting_main import Setting_Main
from .action_eval_main import Action_Eval_Main
from .action_follow_main import Action_Follow_Main
from .Std_show_main import Std_show

# from .test import followtest_Main
__all__ = ['LogMain','Center_Menu_Main','Lessons_Select_Main','Std_Train_Select_Main',
           'Reaction_Train_Main','Setting_Main','Action_Eval_Main',
           'Action_Follow_Main','Std_show',
           'Grade_reaction', 'Grade_std']

