userEmail = input("Enter your email address: ")

slicedEmail = userEmail.split("@")

print(f"The username is {slicedEmail[0]} and the domain is {slicedEmail[1]}")
