function addReplayTableRows(info_rows) {
    function abbreviate_text(text, length, end="...") {
        if(text.length + end.length > length) {
            return text.slice(0, length - end.length) + end;
        } else {
            return text;
        }
    }

    function create_hash_link(prefix, hash, max_length=15) {
        link = document.createElement("a");
        link.href = prefix + hash;
        link.appendChild(document.createTextNode(abbreviate_text(hash, max_length)));
        return link;
    }

    var table_rows = document.getElementById("replayTableBody");

    info_rows.forEach(element => {
        var data_row = document.createElement("tr");
        table_rows.appendChild(data_row);

        var replay = document.createElement("td");
        data_row.appendChild(replay);
        var link = create_hash_link("watch_replay.html?id=", element["replay_hash"]);
        replay.appendChild(link);

        var game = document.createElement("td");
        data_row.appendChild(game);
        var link = create_hash_link("view_script.html?id=", element["game_hash"]);
        game.appendChild(link);

        var player = document.createElement("td");
        data_row.appendChild(player);
        var link = create_hash_link("view_script.html?id=", element["player_hash"]);
        player.appendChild(link);

        var time = document.createElement("td");
        data_row.appendChild(time);
        var text = document.createTextNode(new Date(element["save_time"] * 1000));
        time.appendChild(text);
    });
}