from multiprocessing import Pool
import time

def non_parallel_map_reduce(data):
    start_time = time.time()
    letter_count = {}
    word_count = {}
    for word in data:
        for char in word:
            if char in letter_count:
                letter_count[char] += 1
            else:
                letter_count[char] = 1
        if word in word_count:
            word_count[word] += 1
        else:
            word_count[word] = 1
    end_time = time.time() - start_time
    print(f'Non-parallelized time: {end_time}')
    return {'letters': letter_count, 'words': word_count}

def custom_map(chunk):
    letter_count = {}
    word_count = {}
    for word in chunk:
        for char in word:
            if char in letter_count:
                letter_count[char] += 1
            else:
                letter_count[char] = 1
        if word in word_count:
            word_count[word] += 1
        else:
            word_count[word] = 1
    return {'letters': letter_count, 'words': word_count}

def custom_reduce(results):
    final_letter_count = {}
    final_word_count = {}
    for result in results:
        
        for char, count in result['letters'].items():
            if char in final_letter_count:
                final_letter_count[char] += count
            else:
                final_letter_count[char] = count
        
        for word, count in result['words'].items():
            if word in final_word_count:
                final_word_count[word] += count
            else:
                final_word_count[word] = count
    return {'letters': final_letter_count, 'words': final_word_count}

def parallel_map_reduce(data, Pool_Size):
    chunk_size= len(data) // Pool_Size
    start_time = time.time()
    chunks = [data[i:i+chunk_size] for i in range(0, len(data), chunk_size)]
    with Pool(processes=Pool_Size) as p:
        mapped_results = p.map(custom_map, chunks)
        p.close()
        p.join()
    final_result = custom_reduce(mapped_results)
    endTime = time.time() - start_time
    print(f'Mp time {endTime}')
    return final_result

if __name__ == '__main__':
    
    # Creating data
    Data = ['tarun', 'ramapuram', 'pace', 'university', 'new', 'york', 'city',
            'manhattan', 'the quick brown fox jumps over the lazy dog'] * 100000000

    #Non-parallelized approach
    print("Non-parallelized approach:")
    non_parallel_result = non_parallel_map_reduce(Data)
    print("Letter Counts:", non_parallel_result['letters'])
    print("Word Counts:", non_parallel_result['words'])

    # Parallel MapReduce approach
    print("\nParallel MapReduce approach:")
    parallel_result = parallel_map_reduce(Data, 8)
    print("Letter Counts:", parallel_result['letters'])
    print("Word Counts:", parallel_result['words'])


'''
Report:

    1. Dataset Selection:
        - As advised in the class, we can use the list of words as the data.
          So, I generated a data in the format of list and multiplying it to a number to make
          a big data out of it.
    
    2. Problem Statement:
        - To count the number of times the word occurs in the list and the number of time the each letters occurs.
        - Each Letter Count and Each Word Count
        - Implementing the solution using the Map Reduce method
    
    3. Implement MapReduce:
        1. Use the provided parallel_map_reduce function as a starting point.
            - Implemented the function parallel_map_reduce where it is the starting point of the parallel code implementation.
            - Where the parallel_map_reduce calls the custom_map and custom_reduce.  
            - combines the results from the functions.
            - Implemented the Pool method from the multiprocess to the divide the work among different cores of the processes.
            - I have 8 cores, I have given the number of processes = 8.
            - Based on the no. of processors used, I have divided the data into the Chucks using a simple formula
            - So, these chucks will be given as the input to each job

        2. Develop a custom map function specific to your problem statement.
            - Where we load this function in the pool.map(custom_map, Chuck) which will run the
              function in all the processors in parllel and appends each result from each job
              in mapped_results in form of dictionary.
            - So, at the end the result will have a list of dictionaries of letters and words

        3. Develop a corresponding reduce function.
            - Implemented a function called custom_reduce, which will take the result from the custom_map
            - This function will aggregate the results from custom_map combines all the result into one single result
            - which completes the map reduce functions and will get the result
    
    4. Performance Analysis:
        1. Run the MapReduce job on your dataset and Measure the execution time 
            and compare it with a non-parallelized approach.
            - After running the MapReduce using the Parallel Multiprocessing Approach and 
              Non Parallelized Approach, Results are mentioned below:
                - The Parallel Approach does the task in the half time of the non parallel approach
                - Parallel Approach is faster than the non parallel apporach
                - Parallel Approach is taking 12 Mintues / 744.60889 Seconds
                - Non Parallel Approach is taking 21.6 Mintues /  1266.0496587753296 Seconds


        2. Analyze the scalability of your solution by varying the pool_size parameter.
            - Taking the pool size as the number of processors = 8
                - The results takes to complete 744.60889 Seconds
            - Taking the pool size as the number of processors = 6
                - The results takes to complete 773.663990 Seconds
            - Taking the pool size as the number of processors = 4
                - The results takes to complete 912.587547 Seconds
    
    5. Discuss the scalability and efficiency of the MapReduce model based on your findings.
        - Conculsion : From the above, it is evident that as the Pool size increases the performance also increased
            - As the pool size decreased, The perform also decreased
            - As the Number Cores increases the faster the result that we can except from the above results
    
    6. Reflect on the challenges faced and potential improvements.
        - Finding the logic for Map and Reduce is the Hard Task
        - Deciding what to implement in the Map function using the distribution systems technique to make the result affective
            and as mentioned above finding the right logic is the key for the map and storing the result in the key value pairs is also hard.
        - Should Properly handle the Reduce function to aggregate the result into a single result, Any mistakes in here will lead
            to a wrong result. So implementing the reduce is little complex
        - Improvements can be made like reducing the overhead and reducing the loops in the function instead of that we can use comprehensions.  

 
'''
