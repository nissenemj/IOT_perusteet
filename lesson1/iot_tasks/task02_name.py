# Kysy nimi, tunnista supersankari (ekstra: sallittu lista, casefold)
SUPERS = {"clark kent": "Superman", "bruce wayne": "Batman", "diana prince": "Wonder Woman"}
name = input("Nimesi: ").strip()
hero = SUPERS.get(name.lower())
print("You are the {}!".format(hero) if hero else "You are an ordinary person.")
