def getship(sid):
    return {
        0: "Pilot",
        1: "Starflier",
        2: "Patriot",
        3: "Saber",
        4: "Anubis",
        5: "Aescor Hybrid",
    }[sid]


def getmaxhp(sid):
    return {
        0: "1",
        1: "1000",
        2: "1200",
        3: "1800",
        4: "2500",
        5: "5000",
    }[sid]


def getdamage(wip):
    return {
        0: "0",
        1: "50-150",
        2: "20-160",
        3: "30-180",
        4: "5-400",
        5: "600",
        6: "2500",
    }[wip]


def getacc(wip):
    return {
        0: "N/A",
        1: "40%",
        2: "50%",
        3: "60%",
        4: "70%",
        5: "15%",
        6: "80%",
    }[wip]


def getweapon(wip):
    return {
        0: "None",
        1: "Blaster",
        2: "Type I Repeater",
        3: "Type II Repeater",
        4: "Chaingun",
        5: "Torpedo Launcher Mark I",
        6: "Torpedo Launcher Mark II",
    }[wip] # a series of functions translating ID to names


def getenemyweapon(wip):
    return {
        0: "Unlawful Repeater",
        1: "Deformer",
        2: "Wyrm Class X",
        3: "Bloodhound Mortar",
        4: "Single Barrel Turret",
        5: "Double Barrel Turret",
        6: "Triple Barrel Turret",
        7: "Aescor Cannon",
    }[wip]


def getenemydamage(wip):
    return {
        0: "50-150",
        1: "65-195",
        2: "80-160",
        3: "400",
        4: "100-200",
        5: "200-400",
        6: "400-600",
        7: "350-450",
    }[wip]


def getenemyacc(wip):
    return {
        0: "40%",
        1: "50%",
        2: "60%",
        3: "30%",
        4: "20%",
        5: "25%",
        6: "30%",
        7: "80%",
    }[wip]


def getenemyship(sid):
    return {
        0: "Pirate Interceptor",
        1: "Pirate Fighter",
        2: "Pirate Gunboat",
        3: "Pirate Dreadnaught",
        4: "Aescor Siren",
    }[sid]


def getenemymaxhp(sid):
    return {
        0: "700",
        1: "1000",
        2: "1300",
        3: "2500",
        4: "3500",
    }[sid]
