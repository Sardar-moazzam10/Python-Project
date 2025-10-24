n = int(input("Enter an integer: "))
evens = {n for n in range(2, 5) if n % 2 == 0}
print("Not Weird", evens)
evens2 = {n for n in range(6, 20) if n % 2 == 0}
print("Not Weird", evens2)
if n % 2 != 0:
    print("Weird")
elif n % 2 == 0 and n > 20:
    print("Not Weird")

    

    

# tasks = []
# while True:
#     print("\n Welcome to ToDo List App")
#     print("1. Add Task")
#     print("2. View Tasks")
#     print("3. Delete a Task")
#     print("4. Exit")
    
#     choice = input("Enter your choice (1-4): ")

#     if choice == "1":
#         task = input("Enter task: ")
#         tasks.append(task)
#         print("✅ Task added!")
        
#     elif choice == "2":
#         if not tasks:
#             print(" No tasks found.")
#         else:
#             print(" Your Tasks:")
#             for i, task in enumerate(tasks, start=1):
#                 print(f"{i}. {task}")
#     elif choice == "3":
#           if not tasks:
#                     print(" No tasks to deltete.")   
#           else:
#                 for i, task in enumerate(tasks, start=1):
#                     print(f"{i}. {task}")
#                 try:
#                     option=int(input("Enter the task number to delte:"))
#                     deleted= tasks.pop(option-1)
#                     print(f"Your deletd task are:{deleted}")
#                     print("✅ Task deleted!")
#                 except:
#                     print("Invalid input. Please enter a valid number view your ToDo list.")
#     elif choice == "4":
#             print("Exiting...")
#             break
#     else:
#             print(" Invalid choice. Enter a valid choice like 1,2,3,4.")

