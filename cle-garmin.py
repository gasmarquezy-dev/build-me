# À lancer UNE fois depuis chez toi (iPad avec a-Shell, ou ton PC) :
# il se connecte à Garmin et affiche une longue clé à coller dans GitHub (secret GARMIN_TOKENS).
import getpass
from garminconnect import Garmin
email = input("Email Garmin : ")
mdp = getpass.getpass("Mot de passe Garmin : ")
g = Garmin(email, mdp, prompt_mfa=lambda: input("Code reçu par mail/SMS : "))
g.login()
print("\n=== COPIE TOUT CE QUI SUIT (une seule ligne) ===\n")
print(g.garth.dumps())
