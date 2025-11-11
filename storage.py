import json, os  # fournit la lecture ecriture json et l acces au systeme de fichiers
from typing import Optional  # expose le type optionnel pour une future evolution
from models import Parking, Vehicule  # importe les classes de donnees a serialiser

DATA_FILE = "data.json"  # nom du fichier contenant l etat du parking
CONFIG_FILE = "config.json"  # nom du fichier qui stocke la configuration

DEFAULT_CONFIG = {  # dictionnaire contenant les valeurs par defaut de configuration
    "capacite": 10,  # fixe la capacite initiale du parking
    "tarif_horaire": 2.0  # fixe le tarif horaire initial applique aux sorties
}  # termine la definition du dictionnaire de configuration


def ensure_config():  # garantit que le fichier de configuration existe
    if not os.path.exists(CONFIG_FILE):  # verifie la presence du fichier config
        with open(CONFIG_FILE, "w", encoding="utf-8") as f:  # cree le fichier de configuration en ecriture
            json.dump(DEFAULT_CONFIG, f, ensure_ascii=False, indent=2)  # ecrit les valeurs par defaut formatees


def load_parking() -> Parking:  # charge l etat du parking a partir des fichiers json
    ensure_config()  # s assure que la configuration a ete initialisee
    with open(CONFIG_FILE, "r", encoding="utf-8") as f:  # ouvre la configuration en lecture
        cfg = json.load(f)  # charge les parametres de configuration
    if not os.path.exists(DATA_FILE):  # detecte l absence de sauvegarde des vehicules
        return Parking(capacite=cfg["capacite"], tarif_horaire=cfg["tarif_horaire"], vehicules=[])  # cree un parking vide avec les parametres par defaut
    with open(DATA_FILE, "r", encoding="utf-8") as f:  # ouvre le fichier des donnees persistantes
        d = json.load(f)  # lit l etat sauvegarde
    vehs = [Vehicule(**v) for v in d.get("vehicules", [])]  # reconstruit les vehicules a partir des dictionnaires
    return Parking(capacite=d.get("capacite", cfg["capacite"]),  # recupere la capacite en priorite depuis la sauvegarde
                   tarif_horaire=d.get("tarif_horaire", cfg["tarif_horaire"]),  # recupere le tarif depuis la sauvegarde ou la config
                   vehicules=vehs,  # assigne la liste des vehicules reconstruits
                   recettes_total=d.get("recettes_total", 0.0))  # restaure le total des recettes accumulees


def save_parking(p: Parking) -> None:  # enregistre l etat courant du parking sur disque
    d = {  # constitue la structure de donnees a sauvegarder
        "capacite": p.capacite,  # memorise la capacite actuelle
        "tarif_horaire": p.tarif_horaire,  # memorise le tarif horaire actuel
        "vehicules": [vars(v) for v in p.vehicules],  # convertit chaque vehicule en dictionnaire serialisable
        "recettes_total": p.recettes_total  # stocke le cumul des recettes
    }  # termine la construction du dictionnaire sauvegarde
    with open(DATA_FILE, "w", encoding="utf-8") as f:  # ouvre le fichier des donnees pour ecriture
        json.dump(d, f, ensure_ascii=False, indent=2)  # ecrit le dictionnaire dans le fichier json
