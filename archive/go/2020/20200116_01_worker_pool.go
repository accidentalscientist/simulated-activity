// Archive task: Worker Pool
// Generated for 2020-01-16

package archive

func SumByKey(rows []map[string]int, key string) int {
	total := 0
	for _, row := range rows {
		total += row[key]
	}
	return total
}
