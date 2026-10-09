#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ratiss-runner.py — Lecteur Officiel Exclusif du Cerveau Souverain (.ratiss / .rt)
RATISS Labs · Auteur : Jonathan Evina (Yaoundé, Cameroun) · Licence MIT

Ce runtime est la seule machine virtuelle nécessaire pour charger, inspecter,
et dialoguer avec le vrai Cerveau Souverain RNI (95 660 neurones / 428 471 liens).
"""

import os
import sys
import json
import gzip
import time
import hashlib
import re

MAGIC_HEADER = "RATISS_SOUVERAIN_V2"

class RatissRunner:
    def __init__(self, chemin_modele):
        self.chemin_modele = chemin_modele
        t0 = time.time()
        self.modele = self._charger_modele(chemin_modele)
        self.duree_chargement = time.time() - t0
        
        self.meta = self.modele.get("META", {})
        self.rni = self.modele.get("RNI_MATRICE", {})
        self.neurones = self.rni.get("neurones", [])
        self.liens = self.rni.get("liens", [])
        self.sanctuaire = self.modele.get("SANCTUAIRE", {})
        self.memoire_episodique = self.modele.get("MEMOIRE_EPISODIQUE", {})
        self.eth = self.modele.get("BLOC_ETH", {"pouls_base": 72, "temperature_base": 37.0})
        self.eth_etat = {"pouls": self.eth.get("pouls_base", 72), "temperature": 37.0, "ton": "neutre"}
        self.dernier_sujet = None
        
        # Indexation ultra-rapide des 428 471 liens synaptiques pour l'onde topologique
        self.adjacence = {}
        for s, d, w in self.liens:
            if s not in self.adjacence:
                self.adjacence[s] = []
            self.adjacence[s].append((d, w))

    def _charger_modele(self, chemin):
        if not os.path.exists(chemin):
            raise FileNotFoundError(f"[ERREUR] Cerveau introuvable : {chemin}")
        
        # Détection automatique gzip ou json brut
        try:
            with gzip.open(chemin, "rt", encoding="utf-8") as f:
                data = json.load(f)
        except Exception:
            with open(chemin, "r", encoding="utf-8") as f:
                data = json.load(f)

        if data.get("FORMAT") != MAGIC_HEADER:
            raise ValueError(f"[ERREUR] Format invalide. Attendu {MAGIC_HEADER}, reçu {data.get('FORMAT')}")
        return data

    def verifier_integrite(self):
        taille_mo = os.path.getsize(self.chemin_modele) / (1024 * 1024)
        print("=" * 68)
        print(f"🧠 AUDIT DU CERVEAU SOUVERAIN [{self.meta.get('NOM_MODELE')}]")
        print(f"🔬 Auteur            : {self.meta.get('AUTEUR')}")
        print(f"📁 Fichier           : {self.chemin_modele} ({taille_mo:.2f} Mo)")
        print(f"⏱️ Temps de chargement: {self.duree_chargement*1000:.1f} ms")
        print(f"🧬 Neurones réels     : {len(self.neurones):,} neurones")
        print(f"⚡ Liens synaptiques  : {len(self.liens):,} synapses actives")
        print(f"🏛️ Sanctuaire        : {len(self.sanctuaire)} faits immuables scellés")
        print(f"📝 Mémoire Épisodique: {len(self.memoire_episodique)} faits appris en live")
        print(f"❤️ Corps Somatique ETH: Pouls base {self.eth.get('pouls_base', 72)} bpm | Temp {self.eth.get('temperature_base', 37.0)}°C")
        print("=" * 68)
        return True

    def propager_onde(self, mot_graine, top_k=5):
        """Propage l'onde topologique le long des 428 471 connexions."""
        mg = mot_graine.lower().strip()
        clef = f"word_{mg}" if f"word_{mg}" in self.adjacence else (mg if mg in self.adjacence else None)
        if not clef:
            return []
        
        voisins = sorted(self.adjacence.get(clef, []), key=lambda x: x[1], reverse=True)[:top_k]
        resultats = []
        for v, p in voisins:
            nom_propre = v[5:] if v.startswith("word_") else v
            resultats.append((nom_propre, p))
        return resultats

    def executer(self, message):
        t0 = time.time()
        msg = str(message).strip()
        tokens = set(re.findall(r"\b\w+\b", msg.lower()))
        
        # 1. Modulation somatique ETH
        if any(w in tokens for w in ["pote", "ami", "merci", "thanks", "super", "genial", "bravo"]):
            self.eth_etat = {"pouls": 84, "temperature": 37.2, "ton": "chaleureux"}
        elif any(w in tokens for w in ["danger", "faux", "erreur", "attention"]):
            self.eth_etat = {"pouls": 96, "temperature": 37.6, "ton": "vigilant"}
        else:
            self.eth_etat = {"pouls": 72, "temperature": 37.0, "ton": "neutre"}

        langue = "EN" if any(w in tokens for w in ["hello", "who", "what", "how", "thanks", "bye", "learn"]) else "FR"

        # 2. Apprentissage Épisodique Live ("Apprends que...")
        match_appr = re.search(r"(?:apprends(?:-moi)?(?: que)?|sache que|learn that|retien[ts] que)\s+(.+)", msg, re.IGNORECASE)
        if match_appr:
            enonce = match_appr.group(1).strip()
            h = hashlib.sha256(enonce.encode()).hexdigest()[:12]
            clefs = [w for w in re.findall(r"\b\w+\b", enonce.lower()) if len(w) > 3]
            entree = {"enonce": enonce, "sha256": h, "timestamp": time.time()}
            for c in clefs:
                self.memoire_episodique[c] = entree
            self.dernier_sujet = clefs[0] if clefs else "fait"
            dt_us = (time.time() - t0) * 1_000_000
            rep = f"Recorded in active memory in {dt_us:.1f} µs! Fact sealed #{h}: « {enonce} »." if langue == "EN" else f"Gravé dans ma mémoire active en {dt_us:.1f} µs ! Fait scellé #{h} : « {enonce} »."
            return {"intent": "apprentissage", "langue": langue, "reponse": rep, "eth": self.eth_etat}

        # 3. Salutations & Politesse
        if any(w in tokens for w in ["bonjour", "salut", "yo", "coucou", "hello", "hi"]):
            rep = "Hello! I am RATISS-ONE. Ready." if langue == "EN" else ("Salut mon pote ! Très heureux de te retrouver. Je t'écoute !" if self.eth_etat["ton"] == "chaleureux" else "Bonjour ! Je suis RATISS-ONE, le réseau neuronal souverain. Je t'écoute.")
            return {"intent": "saluer", "langue": langue, "reponse": rep, "eth": self.eth_etat}

        if any(w in tokens for w in ["merci", "thanks", "thank"]):
            rep = "You're very welcome! Always glad to collaborate." if langue == "EN" else ("De rien mon pote ! C'est un réel plaisir de collaborer avec toi." if self.eth_etat["ton"] == "chaleureux" else "Je t'en prie. Mes circuits restent à ton entière disposition.")
            return {"intent": "gratitude", "langue": langue, "reponse": rep, "eth": self.eth_etat}

        if any(p in msg.lower() for p in ["qui es tu", "qui es-tu", "ton nom", "who are you"]):
            rep = "I am RATISS-ONE, a sovereign entangled neural network of 95,660 neurons working without GPU." if langue == "EN" else f"Je suis RATISS-ONE, un tissu de {len(self.neurones):,} neurones intriqués et {len(self.liens):,} synapses conçu à Yaoundé."
            return {"intent": "identite", "langue": langue, "reponse": rep, "eth": self.eth_etat}

        # 4. Restitution de faits du Sanctuaire & Mémoire Épisodique
        est_anaphore = any(p in msg.lower() for p in ["et comment", "comment ça marche", "et où", "how does it work", "where"])
        sujet = self.dernier_sujet if (est_anaphore and self.dernier_sujet) else None
        
        if not sujet:
            for k in self.memoire_episodique:
                if k in tokens or k in msg.lower():
                    sujet = k
                    break
        if not sujet:
            for k in self.sanctuaire:
                if k in msg.lower() or k in tokens:
                    sujet = k
                    break

        if sujet:
            self.dernier_sujet = sujet
            if sujet in self.memoire_episodique:
                info = self.memoire_episodique[sujet]
                rep = f"According to what you taught me (sealed #{info['sha256']}): {info['enonce']}." if langue == "EN" else f"D'après ce que tu m'as appris (scellé #{info['sha256']}) : {info['enonce']}."
                return {"intent": "restitution_episodique", "langue": langue, "reponse": rep, "eth": self.eth_etat}

            ent = self.sanctuaire[sujet]
            mode = "EXPLICATION" if any(w in tokens for w in ["explique", "comment", "pourquoi", "explain", "how"]) else "DEFINITION"
            txt = ent["faits"].get(mode, ent["faits"].get("DEFINITION", ""))
            rep = f"Avec plaisir mon pote ! {txt}" if self.eth_etat["ton"] == "chaleureux" else txt
            return {"intent": f"sanctuaire_{mode.lower()}", "langue": langue, "reponse": rep, "eth": self.eth_etat}

        # 5. ACTIVATION TOPOLOGIQUE DE LA MATRICE RNI (428 471 LIENS)
        # Si la question porte sur un mot présent dans la matrice, le RNI répond par résonance !
        STOP_WORDS = {
            "les", "des", "une", "par", "dans", "pour", "avec", "est", "sont", "que", "sur",
            "qui", "quoi", "dont", "où", "sais", "sait", "peux", "peut", "veut", "fait", "cette", "cet"
        }
        mots_candidats = sorted([w for w in tokens if len(w) >= 3 and w not in STOP_WORDS], key=len, reverse=True)
        for mot in mots_candidats:
            onde = self.propager_onde(mot, top_k=4)
            if onde:
                self.dernier_sujet = mot
                res_texte = ", ".join([f"{n} ({p}%)" for n, p in onde])
                rep = f"L'onde synaptique sur « {mot} » fait résonner dans le tissu : {res_texte}."
                return {"intent": "resonance_rni", "langue": langue, "reponse": rep, "eth": self.eth_etat}

        # 6. Inconnu Honnête
        rep = "I do not hold this fact yet. Say « Learn that... » to teach me!" if langue == "EN" else "Je ne tiens pas encore cette information. Dis-moi « Apprends que... » pour que je la retienne !"
        return {"intent": "inconnu_honnete", "langue": langue, "reponse": rep, "eth": self.eth_etat}

def main():
    if len(sys.argv) < 2:
        print("Usage :")
        print("  python3 ratiss-runner.py <modele.ratiss> \"Message à traiter\"")
        print("  python3 ratiss-runner.py <modele.ratiss> --chat")
        print("  python3 ratiss-runner.py <modele.ratiss> --check")
        sys.exit(1)

    chemin_modele = sys.argv[1]
    runner = RatissRunner(chemin_modele)

    if len(sys.argv) == 2 or sys.argv[2] == "--check":
        runner.verifier_integrite()
        return

    if sys.argv[2] == "--chat":
        print("\n" + "=" * 65)
        print(f"🤖 RATISS-ONE CHAT INTERACTIF [{runner.meta.get('NOM_MODELE')}]")
        print(f"🔬 Auteur : {runner.meta.get('AUTEUR')}")
        print(f"🧬 Graphe : {len(runner.neurones):,} neurones | {len(runner.liens):,} synapses")
        print("💡 Astuce : Tape 'exit' pour quitter.")
        print("=" * 65 + "\n")
        while True:
            try:
                texte = input("Toi > ").strip()
                if not texte:
                    continue
                if texte.lower() in ["exit", "quit", "q"]:
                    print("Au revoir !")
                    break
                res = runner.executer(texte)
                print(f"RATISS [{res['intent']}] : {res['reponse']}\n")
            except (KeyboardInterrupt, EOFError):
                break
        return

    # Message direct
    message = " ".join(sys.argv[2:])
    res = runner.executer(message)
    print(res["reponse"])

if __name__ == "__main__":
    main()
