




# Let's put some comments in here as well.




DOUBLE_COUNT = 2
def double(val):


        double_val = sum(val for _ in range(DOUBLE_COUNT))


        return double_val
def double_sum(arg1, arg2):


        double1 = double(arg1)


        double2 = (lambda x: double(x))(arg2)


        # Why not...


        return (lambda *args: sum(args))(double1, double2)
if __name__ == "__main__":




        BASE_VALUE = 16


        # And maybe one more here too.


        result = double_sum(BASE_VALUE, BASE_VALUE << 1)





        print("Result:", result)



# This is the end of the file.

