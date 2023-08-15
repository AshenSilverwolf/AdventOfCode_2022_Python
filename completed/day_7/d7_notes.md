dictionary references go both ways
- modifying the original reflects changes in the reference
- modifying the reference reflects changes in the original

going backwards through a dictionary
- going deeper into a dictionary is easier
- going backwards is "technically" impossible
    - keep track of the path you took to get to the current directory
    - whenever you encounter a 'cd ..':
        - start at the beginning
        - follow that path to the next-to-last entry
        - remove the last entry