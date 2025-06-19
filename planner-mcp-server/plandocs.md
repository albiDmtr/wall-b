## General Instructions
To control the robot, a script written in Starlark is used to make calls to affordance and utility functions that control the robot. Starlark is a restricted Python-like language where most Python syntax works. Some differences of Starlark compared to Python are:
    - no file system and network access
    - no module imports
    - no while loop (always use for loops)
    - for loops can only be used in `def`s
    - no recursion
    - use 4 spaces (not tabs) per indentation level

## Stopping plan execution and replanning
    To stop plan execution for replanning (for example, when a person has talked to the robot and an appropriate answer needs to be formulated), use `return` (you can only use it at the top-level, outside any functions). The return value will be provided along with program console output (from `print` calls) to aid replanning.
    `find_similar` calls also allow replanning by stopping execution to allow making decisions based on currently seen object labels. It is the preferred way of replanning when trying to find objects with no corresponding COCO labels or potentially mislabeled objects.

## Affordance and Utility Functions
The following functions are exposed to the Starlark environment executing the provided plan:

- Utility Functions:
    - sleep(duration_s) [Number -> None]:
        Halts plan execution for duration_s seconds. Similar to time.sleep().
    - rand_int(min, max) [(Int, Int) -> Int]:
        Returns a random integer number in between min (inclusive) and max (exclusive).

- Affordance Functions:
    - get_objects() [None -> String[]]:
        Returns a list of objects currently seen by the front camera of the robot. Works only with the 80 labels contained in the COCO datset. If the desired object is not found or doesn't have a corresponding COCO label, `find_similar` can provide a more robust solution.
    - find_similar(target)
        Stops code execution and sends target and currently seen objects back for replanning. Similar in effect to `return "Looking for %s, COCO labels seen: %d" % (target, get_objects()) '`
    - move(duration_s, direction) [(Number, 'forward'|'backward') -> None]
        Turns both wheels for duration_s seconds in the required direction.
    - turn(duration_s, side) [(Number, 'left'|'right') -> None]
        Turns the desired wheel on for duration_s seconds in the required direction. It takes around 10 seconds for the robot to do a 180 degree turn.
    - speak(text) [String -> None]:
        Uses the robot's microphones to say the given text.
    - listen(max_duration_s, stop_on_silence=True) [(Number, Boolean) -> String]:
        Takes a maximum duration in seconds as the first argument and an optional second argument
        for stop_on_silence (defaults to True). Listens to people speaking for the specified duration.
        Recording stops if a pause in speech is detected when stop_on_silence is True. Returns the
        transcript of what was heard by the robot, or "" if it didn't hear anything. When having a conversation, it's useful to use the replanning feature to provide customized replies.
    - move_randomly(duration_s) [Number ->None]:
        Move randomly in the area for duration_s seconds to discover new objects while avoiding obstacles.
        Since the robot moves slowly, duration_s should be 30 or more seconds.
    - look_for_object(object_label) [String -> Boolean]
        Uses the camera to look for an object with the required COCO label. The robot rotates to find all objects around it and positions itself to face the required object if found.
    - approach_object(object_label) [String -> Boolean]
        Approaches object with the required COCO label. First, the robot looks for the required object in its surroundings, positions itself to face the required object, then moves forward until the required object is approached.