// Archive task: Json Stream Parser
// Generated for 2021-02-10

package archive

import "encoding/json"

func DecodeObjects(data []byte, target any) error {
	return json.Unmarshal(data, target)
}
