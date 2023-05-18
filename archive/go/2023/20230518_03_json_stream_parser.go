// Archive task: Json Stream Parser
// Generated for 2023-05-18

package archive

import "encoding/json"

func DecodeObjects(data []byte, target any) error {
	return json.Unmarshal(data, target)
}
