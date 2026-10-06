def prn_matrix( matrix):
    for row in matrix:
        print(" ".join(str(x) for x in row))
    print("-" * 33)

#-------------------------
myMatrix =  [ [1,2,3]  \
            ,[4,5,6], \
             [7,8,9]  ]
prn_matrix (myMatrix)
#nicht correct
#myMatrix = [[1] * 5] * 5
# gut add el in matrix
myMatrix = [ [1] * 5 for _ in range(5) ]
myMatrix [1][3] = 3
prn_matrix (myMatrix)