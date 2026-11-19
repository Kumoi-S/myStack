MAGPIE_URL="$(magpie status --json | jq -r '.url // empty')"

curl -fsS "${MAGPIE_URL}/v1/models" | jq -r '
.data[] |
[
  .id,
  ((.reasoning_levels // []) | if length == 0 then "none" else join("/") end)
] | @tsv
' | column -t -s $'\t'
