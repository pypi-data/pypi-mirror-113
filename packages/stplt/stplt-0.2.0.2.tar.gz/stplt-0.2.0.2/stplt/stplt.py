import  numpy as np
print('using terminal_plot v0.1')
def plot_arr(arr,steps=10):
        graph = -np.ones([steps,len(arr)])
        negative_graph = -np.ones([steps,len(arr)])
        maxn=np.max(arr)
        minn = np.min(arr)
     #   print('max value', maxn)
        maparr=np.empty(len(arr)*2)
        col_maped = np.zeros(len(arr))

        for i in range(len(arr)):
                maparr[i]=maxn-arr[i]
        for a in range(steps):
                for i in range(len(arr)):
                        if a != 0:
                                if arr[i] >=0 and arr[i] < 1 :
                                        graph[len(graph)-1][i] = 2
                                        col_maped[i] = 1
                                if arr[i] >= (maxn/steps)*(steps-a)   and col_maped[i] != 1:
                                        graph[a][i] = 1
                                        col_maped[i] = 1
                                        
                        else:
                                if arr[i] == (maxn/steps)*(steps) and col_maped[i] != 1:
                                        graph[a][i] = 1
                                        col_maped[i] = 1
       # print(col_maped)

        for a in range(steps):
                for i in range(len(arr)):
                        if a != 0:
                                if arr[i] >=0 and arr[i] < 1 :
                                        graph[len(graph)-1][i] = 2
                                        col_maped[i] = 1
                                if arr[i] == (minn/steps)*a-1   and col_maped[i] != 1:
                                        negative_graph[a][i] = 1
                                        col_maped[i] = 1
                                        #print(-((minn/steps)*a))
                        else:
                                if arr[i] == (minn/steps)*a-1 and col_maped[i] != 1:
                                        negative_graph[a][i] = 1
                                     #   print(-((minn/steps)*a))
                                        col_maped[i] = 1

        


      #  print("colums : ",len(col_maped))
        print("----graph-----")
        v= ""
        #positive part
        for a in range(steps):
                if a != 0:
                        
                        for i in range(len(arr)):
                                if int(graph[a][i]) == 1 :
                                        v = "■"
                                elif int(graph[a][i]) == 2:
                                        v = "#"
                                      

                                else : v  = "□"
                                print(v,end= "")
                        print("  #",(maxn/steps)*(steps-a))
                        
                else:
                        for i in range(len(arr)):
                                 if int(graph[a][i]) == 1 :
                                        v = "■"
                                 else:
                                        v  = "□"
                                 print(v,end= "")
                        print("  #",(maxn/steps)*steps)
        #negative part 
        for a in range(steps):
                if a != 0:
                        
                        for i in range(len(arr)):
                                if int(negative_graph[a][i]) == 1 :
                                        v = "■"
                                elif int(negative_graph[a][i]) == 2:
                                        v = "#"
                                      

                                else : v  = "□"
                                print(v,end= "")
                        print("  #",(minn/steps)*(a+1))
                        
                else:
                        for i in range(len(arr)):
                                 if int(negative_graph[a][i]) == 1 :
                                        v = "■"
                                 else:
                                        v  = "□"
                                 print(v,end= "")
                        print("  #",-((minn/steps)*a+1))
                #       print(graph.shape)
        print("----values----- from 0 to -> ->",len(col_maped))
        print("this #   are close to 0")
        print("max value",np.max(arr))
        print("min value",np.min(arr))
        print("mean value ",np.mean(arr))
        

def sample():
     print("example using numpy.random.randint from -10 to  10")
     plot_arr(np.random.randint(-10,high=10, size=(20)),5)
        #plot_arr(np.array([5,4,3,2,3,0,3,2,3,4,5]),10)

   

