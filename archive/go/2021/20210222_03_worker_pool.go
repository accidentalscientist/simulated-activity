// Archive task: Worker Pool
// Generated for 2021-02-22

package archive

func RunJobs(jobs []func() int) []int {
	results := make([]int, 0, len(jobs))
	for _, job := range jobs {
		results = append(results, job())
	}
	return results
}
