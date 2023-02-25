# Name : Kevin John Mathew Student No : 201591357
# COMP 517 Assignment 1
# Cache Management

#global lists for cache and requests
cache = list()
requests = list()

def fifo(cache, requests):
  for page in requests:
    if page in cache:
      print('hit')
    else:
      print('miss')
      if len(cache) < 8 :
        cache.append(page)
      else:
          del cache[0]
          cache.append(page)
  return cache


def lfu(cache, requests, requests_dict, min_req_pages) :
  for page in requests:
    requests_dict[page] += 1
    if page in cache:
      print ('Hit')
      continue
    else:
      print('Miss')
      if len(cache) < 8:
        cache.append(page)
      else:
        # create another dictionary with current elements of cache and current count
        request_dict_for_cache = dict((k, requests_dict[k]) for k in cache)

        min_request = min(request_dict_for_cache.values())
        # finding pages that have least frequency 'min_request'
        for key, value in request_dict_for_cache.items():
            if(value == min_request):
              min_req_pages.append(key)
        # finding the smallest number with least frequency
        page_to_be_evicted = min(min_req_pages)
        min_req_pages.clear()
        request_dict_for_cache.clear()
        cache.remove(page_to_be_evicted)
        cache.append(page)
  return cache


def chooseCacheOption():
    while True:
       cacheOption = input("""Choose either option 1 or 2. Press Q to terminate the program
        1. Press 1 for FIFO
        2. Press 2 for LFU
        """)
       if(cacheOption == 'Q'):
        print("Program terminated!")
        exit()

       elif(cacheOption == '1'):
        print("FIFO selected!")
        cache_using_fifo = fifo(cache, requests)
        print(cache_using_fifo)
        # clearing the cache
        cache.clear()
        requests.clear()
        cache_using_fifo.clear()
        inputNumbers(message)
        break

       elif(cacheOption == '2'):
        print("LFU selected!")
        requests_dict = dict.fromkeys(requests, 0)
        min_req_pages = list()
        cache_using_lfu = lfu(cache, requests, requests_dict, min_req_pages)
        print(cache_using_lfu)
        # clearing the cache 
        cache.clear()
        requests.clear()
        cache_using_lfu.clear()
        inputNumbers(message)
        break

       else:
        print("Invalid input! TRY AGAIN")
        continue


def inputNumbers(message):
  while True:
       userInput= input(message)
       if(userInput == '0'):
        print("Sequence of requests complete!")
        break
       try :
        inputNumber = int(userInput)
        if(inputNumber < 0):
          print("Invalid input. Enter a number greater than 0")
          continue
       except ValueError:
        print('Invailed Input. Not an integer!')
        continue
       requests.append(inputNumber)
       print(requests)
  chooseCacheOption()

message = "Enter any positive integer greater than 0. Press 0 to stop the input sequence."
inputNumbers(message)