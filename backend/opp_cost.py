import pandas as pd

def snake_draft(curr_pick, league_size):
    round = (curr_pick - 1) // league_size
    if round%2 == 0:
        position = curr_pick - (league_size * round)
        next_pick = curr_pick + ((league_size - position) * 2) + 1
    else:
        position = (league_size * (round+ 1)) - curr_pick + 1
        next_pick = curr_pick + ((position) * 2) - 1
    return next_pick


def get_best_by_pos(my_rank):
    return my_rank[my_rank.groupby('Position')['HPPR'].transform('max') == my_rank['HPPR']]


def pos_opp_cost(curr_best, next_best):
    return_dict = {}
    for position in ['QB', 'WR', 'TE', 'RB']:
        curr_best_row = curr_best[curr_best['Position'] == position]
        curr_best_hpprpg = curr_best_row['HPPR per Game'].values[0]
        next_best_row = next_best[next_best['Position'] == position]
        next_best_hpprpg = next_best_row['HPPR per Game'].values[0]
        return_dict[position] = {
            'curr_best_name' : curr_best_row['Player Name'].values[0],
            'curr_best_hppr' : curr_best_row['HPPR per Game'].values[0],
            'next_best_name' : next_best_row['Player Name'].values[0],
            'next_best_hppr' : next_best_row['HPPR per Game'].values[0],
            'diff' : curr_best_row['HPPR per Game'].values[0] - next_best_row['HPPR per Game'].values[0]
        }
    return return_dict


def best_options(curr_pick, league_size, my_rank, ecr):
    current_best = get_best_by_pos(my_rank)
    next_round = snake_draft(curr_pick, league_size)
    rounds_to_go = next_round - curr_pick
    get_ecr_picks = ecr['PLAYER NAME'].head(rounds_to_go)
    my_rank = my_rank[my_rank["Player Name"].str.contains('|'.join(list(get_ecr_picks))) == False]
    next_best = get_best_by_pos(my_rank)
    return pos_opp_cost(current_best, next_best)

if __name__ == "__main__":
    my_hppr = pd.read_csv('my_hppr_rank.csv')
    fp_ecr = pd.read_csv('draft_in_progress.csv')
    opp_cost  = best_options(2, 12, my_hppr, fp_ecr)
    print(opp_cost)