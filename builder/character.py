class Personage:
    def __init__(self, nom):
        # prototypeToken
        # token info
        
        # name
        self.nom = nom
        
        # type
        # 'character'
        
        # effects
        # []
        
        # system
        self.attributes = {} # {'hp': {'value': 266, 'temp': 0}, 'speed': {'value': 25, 'otherSpeeds': []}}
        self.initiative = {} # {'statistic': 'perception'}
        self.details = {} # dict_keys(['languages', 'level', 'biography', 'keyability', 'xp', 'age', 'height', 'weight', 'gender', 'ethnicity', 'nationality', 'alliance'])
        self.resources = {} # {'heroPoints': {'value': 1, 'max': 3}, 'focus': {'value': 1}}
        # self._migration = {} # 'version': 0.941, 'previous': {'schema': 0.94, 'foundry': '13.346', 'system': '7.3.1'}}
        self.abilities = None # 'abilities': None,
        self.skills = {} #{'stealth': {'rank': 1}, 'acrobatics': {'rank': 1}, ...}
        # self.pfs = {} # {'playerNumber': None, 'characterNumber': None, 'levelBump': False, 'currentFaction': 'EA', 'school': None, 'reputation': {'EA': None,  'GA': None,  'HH': None,  'VS': None,  'RO': None,  'VW': None}}
        self.exploration = [] # []
        self.build = {} # {'attributes': {'boosts': {'1': ['dex', 'con', 'int', 'cha'], '5': ['int', 'cha', 'dex', 'con'], '10': ['dex', 'con', 'cha', 'int'], '15': ['con', 'int', 'cha', 'dex'], '20': ['con', 'wis', 'dex', 'str']}}}
        # self.crafting = {} # {'formulas': [{'uuid': 'Compendium.pf2e.equipment-srd.Item.zHzAZRDVtl2NFqyh'}, {'uuid': 'Compendium.pf2e.equipment-srd.Item.IhRPEmA2JlYNiCPK'}, {'uuid': 'Compendium.pf2e.equipment-srd.Item.CGmJzsdRb5aJ4eFn'}, {'uuid': 'Compendium.pf2e.equipment-srd.Item.WnNvHEYObRivN1wI'}]}}
        
        # img
        # chemin vers l'image ex: 'systems/pf2e/icons/default-icons/character.svg'

        # items
        # liste de dico :
        self.items = [] # [ Item('_id':, 'img':, 'name':, 'system':, 'type':, '_stats':, 'effects':, 'folder':, 'sort':, 'flags':), ...]
        
        # folder
        # None
        
        # flags
        # {}
        
        # _stats
        # {'coreVersion': '13.347', 'systemId': 'pf2e', 'systemVersion': '7.3.1', ...




class Item:
    def __init__(self, _id, img, name, system, type, _stats, effects, folder, sort, flags):
        self._id = _id
        self.img = img
        self.name = name
        self.system = system
        
        self.type = type
        # {'action': 4,
        # 'ancestry': 1,
        # 'background': 1,
        # 'class': 1,
        # 'consumable': 1,
        # 'deity': 1,
        # 'feat': 65,
        # 'heritage': 1,
        # 'spell': 13,
        # 'spellcastingEntry': 2,
        # 'weapon': 2}
        
        self._stats = _stats
        self.effects = effects
        self.folder = folder
        self.sort = sort
        self.flags = flags

