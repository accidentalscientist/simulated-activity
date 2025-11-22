// Archive task: Json Stream Parser
// Generated for 2025-11-22

package archive

import "encoding/json"

func DecodeObjects(data []byte, target any) error {
	return json.Unmarshal(data, target)
}
