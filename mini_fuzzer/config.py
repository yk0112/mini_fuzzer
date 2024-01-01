
# executable file  directory 
EX_DIRECTORY = '../build'

# list of arguments that will not be mutated
SKIP_ARGS = [0]

# for arithmetic inc or dec in mutation
INCREMENT_VALUE = 30
DECREMENT_VALUE = 30


# for add_interesting_value in mutation
INTERESTING_VALUE = [
  -128,          # Overflow signed 8-bit when decremented  
  -1,                                                     
   0,                                                     
   1,                                                     
   16,           # One-off with common buffer size         
   32,           # One-off with common buffer size         
   64,           # One-off with common buffer size         
   100,          # One-off with common buffer size         
   127,          # Overflow signed 8-bit when incremented  
  -32768,        # Overflow signed 16-bit when decremented 
  -129,          # Overflow signed 8-bit                   
   128,          # Overflow signed 8-bit                   
   255,          # Overflow unsig 8-bit when incremented   
   256,          # Overflow unsig 8-bit                    
   512,          # One-off with common buffer size         
   1000,         # One-off with common buffer size         
   1024,         # One-off with common buffer size         
   4096,         # One-off with common buffer size         
   32767         # Overflow signed 16-bit when incremented 
  -2147483648,   # Overflow signed 32-bit when decremented 
  -100663046,    # Large negative number (endian-agnostic) 
  -32769,        # Overflow signed 16-bit                  
   32768,        # Overflow signed 16-bit                  
   65535,        # Overflow unsig 16-bit when incremented  
   65536,        # Overflow unsig 16 bit                   
   100663045,    # Large positive number (endian-agnostic) 
   2147483647    # Overflow signed 32-bit when incremented 
]
