# Wall-B JSON DSL Docs

Wall-B is instructed through a custom JSON DSL (domain-specific language) consisting of a couple of operators,
statements, and affordance functions.

### Operator blocks:
- `==`(euqality, requires left and right operands)
- `>` (bigger than, requires left and right operands)
- `<` (smaller than, requires left and right operands)
- `!` (not, requires right operand only)
- `>=` (bigger or equal, requires left and right operands)
- `<=` (smaller or equal, requires left and right operands)
- `in` (to check if a list contains an element, requires left and right operands)

(operators work with an number, string, boolean or array literal, variable, or return values of function calls)

The structure of an operator block is as follows:
'''
{
    "type": ">=",
    "leftOperand": 1
    "rightOperand": 3
}
'''

### Statement blocks:
- `if` (if statement)
    - Stucture:
        '''
        {
            "type": "if",
            "condition": {}
            "body":[]
        }
        '''
        Where `condition` can only contain operators and affordance calls, and `body` can contain arbitrary code. 
- `elif` (else if statement, only valid after if statement)
    - Stucture:
        '''
        {
            "type": "elif",
            "condition": {}
            "body":[]
        }
        '''
        Where `condition` can only contain operators and affordance calls, and `body` can contain arbitrary code.
- `else` (else statement, only valid after if or elif statement)
    - Stucture:
        '''
        {
            "type": "else",
            "body":[]
        }
        '''
        Where `body` can contain arbitrary code.  
- `while` (while loop)
    - Stucture:
        '''
        {
            "type": "while",
            "condition": {}
            "body":[]
        }
        '''
        Where `condition` can only contain operators and affordance calls, and `body` can contain arbitrary code.
- `var` (variable assignment or access)
    - Stucture:
        '''
        {
            "type": "var",
            "name": "foo"
            "value": "bar"
        }
        '''
        Where `name` has to be a string that is not a reserved keyword and doesn't start with a number, and `value` has to be a number, string, boolean, array, or a function call. If `value` field is present, the block is interpreted as assignment to a variable name, if not, the block returns the value of the variable.
- `sleep` (halts program execution for a given amount of time in seconds)
        - Stucture:
            '''
            {
                "type": "sleep",
                "duration_s": 2
            }
            '''
            Where `duration_s` is a float or integer number.
- `return` (returns program)
        - Stucture:
            '''
            {
                "type": "return",
                "message": "execution unsuccessful, maximum number of attempts reached"
            }
            '''
            Where `message` is the message that will be returned when the program exits.
        

The structure of a statement block is as follows:
'''
{
    "type": "if",
    "condition": {}
    "body":[]
}
'''

### Affordance blocks:
- `get_objects` (Returns a list of objects currently seen by the front camera of the robot)
    - Stucture:
        '''
        {
            "type": "get_objects",
        }
        '''
- `approach` (Approach a given object seen by the camera. Returns True is action was successfull)
    - Stucture:
        '''
        {
            "type": "approach",
            "object": "laptop"
        }
        '''
        Where `object` has to exactly match an object label currently seen by the camera.
- `move_randomly` (Move randomly in the area for duration_s seconds to discover new objects while avoiding obstacles)
    - Stucture:
        '''
        {
            "type": "move_randomly",
            "duration_s": 5
        }
        '''
- `listen` (Listens to people speaking for duration_s seconds. Returns the transcript of what was heard by the robot, or "" if it didn't hear anything)
        - Stucture:
        '''
        {
            "type": "listen",
            "duration_s": 3.5
        }
        '''
- `speak` (Uses the robot's microphones to say the given text. Returns True if action was successful)
        - Stucture:
        '''
        {
            "type": "speak",
            "text": "Hello! Welcome to the office!"
        }
        '''

## General structure of a DSL Object:
DSL Objects always start with a main block that contains the script inside of it, in the form of an array of objects:
'''
{
    "type": "main",
    "body": [...]
}
'''

Inside the script body, blocks are chained or nested into each other.

## Example code
The following is an example code used to find people and greet them:
```
{
    "type": "main",
    "body": [
        {
            "type": "while",
            "condition": true
            "body": [
                {
                    "type": "var",
                    "name": "objects"
                    "value": {
                        "type": "get_objects"
                    }
                },
                {
                    "type": "if",
                    "condition": {
                        "type": "!",
                        "rightOperand": {
                            {
                                "type": "in",
                                "leftOperand": "person",
                                "rightOperand": {
                                    "type": "var",
                                    "name": "objects"
                                }
                            }
                        }
                    }
                    "body": [
                        {
                            "type": "move_randomly
                        }
                    ]
                },
                {
                    "type": "else",
                    "body": [
                        {
                            "type": "approach",
                            "object": "person"
                        },
                        {
                            "type": "speak",
                            "text": "Hello! Welcome to the office!"
                        },
                        {
                            "type": "var",
                            "name": "response",
                            "value": {
                                "type": "listen",
                                "duration_s": 3
                            }
                        },
                        {
                            "type": "if",
                            "condition": {
                                "type": "var",
                                "name": "response"
                            },
                            "body": [
                                {
                                    "type": "return",
                                    "message": response
                                }
                            ]
                        },
                        {
                            "type": "else",
                            "body": [
                                {
                                    "type": "move_randomly",
                                    "duration_s": 5
                                }
                            ]
                        }
                    ]
                }
            ]
        }
    ]
}
```

Which is equivalent to the following Python code:
```
while True:
    objects = get_objects()
    if not 'person' in objects:
        move_randomly(5)
    else:
        approach('person')
        speak('Hello! Welcome to the office!')
        response = listen(3)
        if response:
            return response
        else:
            move_randomly(5)
```