from itertools import combinations_with_replacement
import math

def generate_arrangements(intervals, max_length):
    print("yes")
    # Generate all possible combinations of the intervals
    for r in range(1, max_length + 1):
        for combination in combinations_with_replacement(intervals, r):
            yield combination

def arrange_intervals(intervals, max_length):
   
    # Generate all possible arrangements and sort them by total length
    arrangements = list(generate_arrangements(intervals, max_length))
    arrangements.sort(key=sum)

    # Yield the arrangements in order of increasing total length
    for arrangement in arrangements:
        
        yield arrangement

def main():
    intervals = [4,7,13]
    max_length = 4
    
    arrangements = arrange_intervals(intervals, max_length)
    for arrangement in arrangements:
        if sum(arrangement) < 20:
            print(arrangement)
   
if __name__ == '__main__':
    main()