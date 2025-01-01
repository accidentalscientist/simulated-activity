// Archive task: Json Stream Parser
// Generated for 2025-01-01

package archive

import "encoding/json"

func DecodeObjects(data []byte, target any) error {
	return json.Unmarshal(data, target)
}
