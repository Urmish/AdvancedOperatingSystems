
function parse_results {
    grep 'Pages:' $1.log |awk '{print $2, ",", $5}' > $1.csv
}
