from dataclasses import dataclass, asdict  # importe les outils pour definir des dataclasses et les convertir en dictionnaires
from datetime import datetime, timedelta  # fournit les classes pour manipuler les dates et les delais
from typing import Optional, List, Dict  # ajoute les annotations de type utilisees dans ce module
import math  # offre des fonctions mathematiques comme l arrondi superieur

ISO_FMT = "%Y-%m-%dT%H:%M:%S"  # definit le format iso commun pour stocker les horodatages


def now_str() -> str:  # retourne l horodatage courant formate
    return datetime.now().strftime(ISO_FMT)  # formate l instant actuel selon le format iso


def parse_dt(s: str) -> datetime:  # convertit une chaine iso en objet datetime
    return datetime.strptime(s, ISO_FMT)  # interprete la chaine selon le format defini


@dataclass  # transforme la classe suivante en dataclass pour reduire le code ceremoniel
class Vehicule:  # represente un vehicule suivi par le parking
    immatriculation: str  # stocke la plaque du vehicule
    entree: str  # enregistre l horodatage d entree au format iso
    sortie: Optional[str] = None  # conserve l horodatage de sortie ou None tant que le vehicule est present

    def est_gare(self) -> bool:  # indique si le vehicule est toujours stationne
        return self.sortie is None  # verifie si aucun horaire de sortie n a ete defini

    def duree_minutes(self) -> int:  # calcule la duree de stationnement en minutes
        end = parse_dt(self.sortie) if self.sortie else datetime.now()  # recupere la date de fin en fonction de la sortie
        start = parse_dt(self.entree)  # convertit l horodatage d entree en datetime
        return max(0, int((end - start).total_seconds() // 60))  # retourne la duree en minutes en evitant les valeurs negatives


@dataclass  # transforme la classe suivante en dataclass pour simplifier les initialisations
class Parking:  # modele representant le parking complet
    capacite: int  # nombre total de places disponibles
    tarif_horaire: float  # tarif facture par heure
    vehicules: List[Vehicule]  # liste des vehicules suivis
    recettes_total: float = 0.0  # montant cumule des recettes

    def places_disponibles(self) -> int:  # calcule le nombre de places libres
        garés = sum(1 for v in self.vehicules if v.est_gare())  # compte les vehicules encore stationnes
        return max(0, self.capacite - garés)  # soustrait les vehicules presents de la capacite totale

    def entrer(self, immat: str) -> str:  # gere l entree d un nouveau vehicule
        if self.places_disponibles() <= 0:  # verifie si le parking est complet
            return "Parking complet."  # indique l impossibilite d entrer
        if any(v.est_gare() and v.immatriculation == immat for v in self.vehicules):  # evite les doublons pour la meme plaque
            return "Ce véhicule est déjà dans le parking."  # avertit que le vehicule est deja present
        self.vehicules.append(Vehicule(immatriculation=immat.upper(), entree=now_str()))  # ajoute le vehicule avec l heure d entree courante
        return f"Entrée enregistrée pour {immat.upper()}."  # confirme l ajout du vehicule

    def sortir(self, immat: str) -> str:  # gere la sortie d un vehicule existant
        for v in self.vehicules:  # parcourt tous les vehicules connus
            if v.est_gare() and v.immatriculation == immat.upper():  # recherche le vehicule correspondant encore gare
                v.sortie = now_str()  # enregistre l horodatage de sortie
                montant = self.calcul_tarif(v)  # calcule le montant a facturer
                self.recettes_total += montant  # ajoute le montant aux recettes totales
                return (f"Sortie {immat.upper()} | Durée: {v.duree_minutes()} min | "  # retourne un message detaille sur la sortie
                        f"Tarif: {self.tarif_horaire:.2f}€/h | Total: {montant:.2f}€")  # complete le message avec le tarif et le total
        return "Véhicule non trouvé ou déjà sorti."  # indique que le vehicule n a pas ete localise

    def calcul_tarif(self, v: Vehicule) -> float:  # calcule le prix a regler pour un vehicule donné
        minutes = v.duree_minutes()  # recupere la duree en minutes
        heures = math.ceil(minutes / 60.0)  # arrondit la duree a l heure superieure
        return round(heures * self.tarif_horaire, 2)  # calcule le total arrondi a deux decimales

    def liste_garés(self) -> List[Dict]:  # fournit la liste des vehicules encore stationnes
        return [asdict(v) for v in self.vehicules if v.est_gare()]  # convertit les vehicules actifs en dictionnaires
