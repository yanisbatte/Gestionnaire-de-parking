
from storage import load_parking, save_parking  # importe les fonctions de chargement et de sauvegarde du parking
from models import Parking  # importe la classe representant le parking


def banner(p: Parking):  # affiche le menu principal avec l etat actuel du parking
    print("=== Parking Simulator ===")  # affiche le titre du simulateur
    print(f"Places dispo : {p.places_disponibles()} / {p.capacite}")  # affiche les places libres restantes
    print("1. Entrée véhicule")  # propose l option d enregistrer une entree
    print("2. Sortie véhicule")  # propose l option d enregistrer une sortie
    print("3. Liste véhicules garés")  # propose d afficher les vehicules gares
    print("4. Total recettes")  # propose d afficher les recettes totales
    print("5. Modifier paramètres (capacité, tarif)")  # propose de modifier les parametres
    print("6. Quitter")  # propose de quitter l application


def main():  # lance la boucle principale de l application
    p = load_parking()  # charge l etat persistant du parking
    while True:  # boucle jusqu a ce que l utilisateur quitte
        banner(p)  # affiche le menu avant chaque choix
        try:  # capture les exceptions de saisie utilisateur
            ch = input("> ").strip()  # lit et nettoie le choix de l utilisateur
        except (EOFError, KeyboardInterrupt):  # gere la fin de fichier ou l interruption clavier
            print("\nSortie...")  # informe que le programme se ferme
            break  # quitte la boucle principale
        if ch == "1":  # traite l option d entree d un vehicule
            immat = input("Immatriculation : ").strip()  # demande la plaque du vehicule a faire entrer
            if not immat:  # verifie que la plaque n est pas vide
                print("Entrée invalide.")  # indique que la saisie est vide
                continue  # retourne au menu sans action
            print(p.entrer(immat))  # tente d enregistrer l entree et affiche le resultat
            save_parking(p)  # enregistre l etat apres l entree
        elif ch == "2":  # traite l option de sortie d un vehicule
            immat = input("Immatriculation : ").strip()  # demande la plaque du vehicule a faire sortir
            if not immat:  # verifie que la plaque n est pas vide
                print("Entrée invalide.")  # indique que la saisie est vide
                continue  # retourne au menu sans action
            print(p.sortir(immat))  # tente d enregistrer la sortie et affiche le resultat
            save_parking(p)  # enregistre l etat apres la sortie
        elif ch == "3":  # traite l option d afficher les vehicules encore garés
            garés = p.liste_garés()  # recupere la liste des vehicules encore presents
            if not garés:  # verifie si aucun vehicule n est present
                print("Aucun véhicule garé.")  # informe qu aucune voiture n est stationnee
            else:  # gere le cas ou au moins un vehicule est present
                for v in garés:  # parcourt chaque vehicule encore stationne
                    print(f"- {v['immatriculation']} (entrée {v['entree']})")  # affiche la plaque et l heure d entree
        elif ch == "4":  # traite l option d afficher les recettes
            print(f"Recettes totales : {p.recettes_total:.2f}€")  # affiche la somme des recettes
        elif ch == "5":  # traite l option de modification des parametres
            try:  # capture les erreurs liees aux conversions numeriques
                cap = int(input(f"Nouvelle capacité (actuelle {p.capacite}) : ").strip() or p.capacite)  # lit la nouvelle capacite ou conserve l ancienne
                tarif = float(input(f"Tarif horaire (actuel {p.tarif_horaire} €/h) : ").strip() or p.tarif_horaire)  # lit le nouveau tarif ou conserve l ancien
                if cap < 0 or tarif < 0:  # valide que les valeurs sont positives
                    print("Valeurs invalides.")  # refuse les valeurs negatives
                    continue  # retourne au menu sans changer les parametres
                p.capacite, p.tarif_horaire = cap, tarif  # met a jour la capacite et le tarif
                print("Paramètres mis à jour.")  # confirme la mise a jour
                save_parking(p)  # enregistre les nouveaux parametres
            except ValueError:  # capture toute erreur de conversion
                print("Entrée invalide.")  # signale une saisie numerique incorrecte
        elif ch == "6":  # traite l option de quitter le programme
            print("À bientôt.")  # affiche un message d au revoir
            break  # sort de la boucle et termine le programme
        else:  # gere tous les autres choix non valides
            print("Choix invalide.")  # indique que le choix n est pas reconnu


if __name__ == "__main__":  # assure l execution seulement si le script est lance directement
    main()  # execute la fonction principale
