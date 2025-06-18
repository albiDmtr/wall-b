import starlark as sl
import time
import random
from move.motor_driver import move_s, turn_s
from object_detection.efficientdet import EfficientDet
from cam.stereo_cam import stereo_cam
from cam.stereo_processing import undistort_rectify
from speak.speak import speak

class PlanInterpreter:
    def __init__(self):
        self._cam = stereo_cam()
        self._cam.start()
        self._detector = EfficientDet()
        self._speak_listen = speak()

        self._sl_glb = sl.Globals.standard()
        self._sl_mod = sl.Module()
        self._sl_mod.add_callable("sleep", self._sleep)
        self._sl_mod.add_callable("rand_int", self._rand_int)
        self._sl_mod.add_callable("print", self._print)
        self._sl_mod.add_callable("move", move_s)
        self._sl_mod.add_callable("turn", turn_s)
        self._sl_mod.add_callable("get_objects", self._get_objects)
        self._sl_mod.add_callable("find_similar", self._find_similar)
        self._sl_mod.add_callable("speak", self._speak_listen.speak)
        self._ast = None

        self._current_logs = 'Execution logs:\n\n'
        self._prefix = 'def main():\n'
        self._suffix = '\nprint(main())'
    
    def _get_objects(self):
        img = self._cam.capture()
        left, right = undistort_rectify(img)
        objects = self.detector.detect(left)
        objects_list = [obj['label'] for obj in sorted(objects, key=lambda x: x['score'], reverse=True)]
        
        return objects_list

    def _sleep(self, seconds):
        time.sleep(seconds)

    def _rand_int(self, min_val, max_val):
        return random.randint(min_val, max_val)
    
    def _print(self, message):
        if message is None:
            message = ''
        self._current_logs +=str(message) + '\n'
    
    def _find_similar(self, obj):
        scene_objects = self._get_objects()
        self._current_logs += f'\nPlan execution stopped due to find_similar call.\nFind similar objects to {obj} in current scene containing the following COCO labels: {scene_objects}\n'
    
    def _add_tabs(self, plan, num_tabs):
        return ' '*(4*num_tabs) + plan.replace('\n', ('\n'+' '*(4*num_tabs)))
    
    def _add_return_after_call(self, plan, fun_name):
        result = []
        lines = plan.split('\n')

        for line in lines:
            result.append(line)
            if f'{fun_name}(' in line:
                indentation = len(line) - len(line.lstrip())
                result.append(' ' * indentation + 'return')

        return '\n'.join(result)

    def execute(self, plan):
        modified_plan = self._add_return_after_call(plan, 'find_similar')
        extended_plan = self._prefix + self._add_tabs(modified_plan, 1) + self._suffix

        print("Executing plan:")
        print(extended_plan)

        try:
            self._sl_ast = sl.parse("wall-b-plan", extended_plan)

            try:
                sl.eval(self._sl_mod, self._sl_ast, self._sl_glb)
                self._current_logs += "[Plan executed successfully]\n"
            except Exception as e:
                self._current_logs += f"Runtime error: {str(e)}\n"
        except Exception as e:
            self._current_logs += f"Parse error: {str(e)}\n"

        logs = self._current_logs
        self._current_logs = 'Execution logs:\n\n'

        print(logs)

        return logs