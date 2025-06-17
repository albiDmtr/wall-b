## General Instructions
To control the robot, a script written in Starlark is used to make calls to affordance and utility functions that control the robot. Starlark is a restricted Python-like language where most Python syntax works. Some differences of Starlark compared to Python are:
    - no file system and network access
    - no module imports
    - no while loop (always use for loops)
    - for loops can only be used in `def`s
    - no recursion
    - use 4 spaces (not tabs) per indentation level

## Stopping plan execution and replanning
    The generated starlark code is run inside a main function. To stop plan execution for replanning (for example, when a person has talked to the robot and an appropriate answer needs to be formulated), use `return`. The return value will be provided along with program console output (from `print` calls) to aid replanning.

## Affordance and Utility Functions
The following functions are exposed to the Starlark environment executing the provided plan:

- Utility Functions:
    - sleep(duration_s) [Number -> None]:
        Halts plan execution for duration_s seconds. Similar to time.sleep().
    - rand_int(min, max) [(Int, Int) -> Int]:
        Returns a random integer number in between min (inclusive) and max (exclusive).

- Affordance Functions:
    - get_objects() [None -> String[]]:
        Returns a list of objects currently seen by the front camera of the robot
    - approach(object) [String -> Bool]:
        Approach a given object seen by the camera. Returns True is action was successfull.
    - move_randomly(duration_s) [Number -> None]:
        Move randomly in the area for duration_s seconds to discover new objects while avoiding obstacles.
    - listen(duration_s) [Number -> String]:
        Listens to people speaking for duration_s seconds. Returns the transcript of what was heard by the robot, or "" if it didn't hear anything.
    - speak(text) [String -> Bool]:
        Uses the robot's microphones to say the given text. Returns True if action was successful.