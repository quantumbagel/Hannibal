

class Leaderboard:
    def __init__(self, leaderboard):
        self.leaderboard_driver = leaderboard
        self.leaderboard = []
        self.update()

    def update(self):
        outer_html = self.leaderboard_driver.get_attribute('outerHTML'). \
            replace('<table id="game-leaderboard"><tbody><tr><td><span style="white-space: nowrap;"><span '
                    'style="color: gold;">★ </span></span></td><td>Player</td><td>Army</td><td>Land</td></tr><tr '
                    'class=""><td> <span style="white-space: nowrap;"><span style="color: gold;"> ', "").replace(
            "</tr>", ""). \
            replace('"', "").replace('<tr>', "")
        leaderboard = [[j.replace("</td><tr class=><td> ", "")
                        .replace("</td></tbody></table>", "")
                        .replace("</span>", "")
                        .replace("</td><td class=leaderboard-name ", "")
                        for j in i.split("</td><td>")] for i in
                       outer_html.replace("<span style=white-space: nowrap;><span style=color: gold;>", "").split("★")][
                      2:]
        self.leaderboard = {}
        for leader in leaderboard:
            lead = {}
            name = leader[0].split(">")
            lead['color'] = name[0].split(" ")[2]
            lead['name'] = name[1]
            lead['troops'] = leader[1]
            lead['land'] = leader[2].split("<")[0]
            lead['rank'] = leader[0].split(" ")[1]
            self.leaderboard.update({lead['name']: {'land': lead['land'], 'troops': lead['troops'],
                                                    'color': lead['color'], 'rank': lead['rank']}})
