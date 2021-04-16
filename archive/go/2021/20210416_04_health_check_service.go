// Archive task: Health Check Service
// Generated for 2021-04-16

package archive

type HealthCheck struct {
	Name string
	OK   bool
}

func OverallStatus(checks []HealthCheck) bool {
	for _, check := range checks {
		if !check.OK {
			return false
		}
	}
	return true
}
