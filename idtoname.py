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
        -1: "0",
        0: "50-150",
        1: "20-160",
        2: "30-180",
        3: "5-400",
        4: "600",
        5: "2500",
    }[wip]


def getacc(wip):
    return {
        -1: "N/A",
        0: "40%",
        1: "50%",
        2: "60%",
        3: "70%",
        4: "15%",
        5: "80%",
    }[wip]


def getweapon(wip):
    return {
        -1: "None",
        0: "Blaster",
        1: "Type I Repeater",
        2: "Type II Repeater",
        3: "Chaingun",
        4: "Torpedo Launcher Mark I",
        5: "Torpedo Launcher Mark II",
    }[wip] # a series of functions translating ID to names