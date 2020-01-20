// Archive task: Json Stream Parser
// Generated for 2020-01-20

package archive

func SumByKey(rows []map[string]int, key string) int {
	total := 0
	for _, row := range rows {
		total += row[key]
	}
	return total
}
