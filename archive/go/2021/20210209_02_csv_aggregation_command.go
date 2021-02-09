// Archive task: Csv Aggregation Command
// Generated for 2021-02-09

package archive

func SumByKey(rows []map[string]int, key string) int {
	total := 0
	for _, row := range rows {
		total += row[key]
	}
	return total
}
