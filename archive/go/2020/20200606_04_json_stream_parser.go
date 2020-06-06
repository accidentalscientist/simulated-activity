// Archive task: Json Stream Parser
// Generated for 2020-06-06

package archive

import "encoding/json"

func DecodeObjects(data []byte, target any) error {
	return json.Unmarshal(data, target)
}
