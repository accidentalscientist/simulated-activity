// Archive task: Json Stream Parser
// Generated for 2022-02-14

package archive

import "encoding/json"

func DecodeObjects(data []byte, target any) error {
	return json.Unmarshal(data, target)
}
