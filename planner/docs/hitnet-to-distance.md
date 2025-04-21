# Hitnet values to real-world distance of an object

## With current stereo camera:
- Box:
    - 30cm → 97
    - 60cm → 72
    - 90cm → 53
    - 120cm → 41.5
    - 180cm → 30
- Wall:
    - 120cm → 42.5
    - 180cm → 31
    - 240cm → 24
    - 300cm → 20.5
    - 360cm → 19
- Wall angles:
    - 180cm angle 1 → 43
    - 180cm angle 2 → 34


## Formula to get distance (Z) from disparity (d):
Z = (f * B) / (d - d₀)

## How to get f*B and d_0:
- By plotting 1/distance agains the disparity values (the x axis being 1/distance) and using linear regression
- The slope is f*B, and the y-intercept is d_0

```
f*B: 38.94
d_0: 8.57
```

Based on this: Z = 38.94*(disparity - 8.57)
(Where Z is distance in meters)

## Formula prediction results:
```
- Box:
    - 60cm → 72
        - Formula says: 61cm
    - 90cm → 53
        - Formula says: 88cm
    - 120cm → 41.5
        - Formula says: 118cm
    - 180cm → 30
        - Formula says: 182cm
- Wall:
    - 120cm → 42.5
        - Formula says: 115cm
    - 180cm → 31
        - Formula says: 174cm
    - 240cm → 24
        - Formula says: 252cm
    - 300cm → 20.5
        - Formula says: 326cm
    - 360cm → 19
        - Formula says: 373cm
- Wall angles:
    - 180cm angle 1 → 43
        - Formula says: 113cm
    - 180cm angle 2 → 34
        - Formula says: 153cm
```