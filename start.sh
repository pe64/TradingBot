tmux new -s charge -d
tmux send -t charge "python3 src/asset_charge.py" Enter

tmux new -s policy -d
tmux send -t policy "python3 src/policy.py" Enter

tmux new -s account -d
tmux send -t account "python3 src/account.py" Enter

tmux new -s login -d
tmux send -t login "python3 src/em_login.py" Enter