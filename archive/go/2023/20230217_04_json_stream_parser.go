// Archive task: Json Stream Parser
// Generated for 2023-02-17

package archive

import "encoding/json"

func DecodeObjects(data []byte, target any) error {
	return json.Unmarshal(data, target)
}
