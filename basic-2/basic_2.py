"""
Assegnamento 2 di cmepda:
Scrivere un metodo che implementi una classe per descrivere una particella generica.

Antoine Venturini e Marco Riggirello
"""

import logging

import math


class Particle:
    """
    Class describing a generic particle through this properties:
    mass, charge, name, momentum
    """
    def __init__(self, mass, charge, name, momentum = 0.):
        """mass= massa della particella espressa in Mev/c^2
           charge=carica della particella in unità di e
           name=nome della particella
           momentum=impulso della particella in unità di MeV/c
           """
        self.mass = mass
        self.charge = charge
        self.name = name
        self.momentum = momentum

    def info(self):
        """Stampa le 4 proprietà della particella"""
        information = 'Particle {} of mass {} MeV c^2, charge {} and momentum {} MeV/c'
        return information.format(self.name, self.mass, self.charge, self.momentum)

    def __repr__(self):
        """Metodo speciale per stampare informazioni sugli
        oggetti di questa classe.
        """
        return f"{Particle}(name = {self.name}, mass = {self.mass},\
                charge = self.charge, momentum = {self.momentum})"

    @property
    def energy(self):
        """Energia della particella in MeV
        """
        return math.sqrt(self.mass**2 + self.momentum**2)

    @energy.setter
    def energy(self, energy):
        """Inserisce l'energia della particella, con un check sul valore.
        """
        if energy<self.mass:
            logging.error("Viola la relazione di Einstein!")
        else:
            self.momentum = math.sqrt(energy**2-self.mass**2)

    @property
    def momentum(self):
        """Setting momentum as a property.
        """
        return self._momentum

    @momentum.setter
    def momentum(self, momentum):
        """Controlla che il momento definito dall'utente sia valido.
        """
        if momentum <0.:
            logging.error("Impulso negativo!")
        else:
            self._momentum = momentum

    @property
    def beta(self):
        """Defining beta parameter for the particle.
        """
        return self.momentum/self.energy

    @beta.setter
    def beta(self, beta):
        """
        Controlla che il beta dell'utente sia valido.
        Ridefinisce il momento della particella a partire dal beta.
        """
        if beta <0. or beta >1.:
            logging.error("Valore errato per beta!")
        else:
            self.momentum = beta*(1/(math.sqrt(1-beta**2)))*self.mass


class Proton(Particle):
    """
    Classe che descrive una Particle chiamata Protone
    con le sue proprietà di particella.
    """
    NAME = 'Proton'
    MASS = 937 #MeV c^2
    CHARGE = +1 #e

    def __init__(self, momentum=0.):
        super().__init__(self.NAME, self.MASS, self.CHARGE, momentum)


class Alpha(Particle):
    """
    Classe che descrive una Particle chiamata Alpha con le sue proprietà di particella.
    """
    NAME = 'Alpha particle'
    MASS = 3600 #MeV c^2
    CHARGE = +2 #e

    def __init__(self, momentum=0.):
        super().__init__(self.MASS, self.CHARGE, self.NAME,  momentum)
