package llm

import (
	"bytes"
	"encoding/json"
	"net/http"
)

type Message struct {
	Role string `json:"role"`
	Content string `json:"content"`
}


func getApiUrl(path string) string {
	return "http://localhost:6061" + path
}


func ChatWithRole(message Message, role string)  string {
	body := map[string]interface{}{
		"messages": []Message{message},
	}

	bytesData, _ := json.Marshal(body)


	const contentType = "application/json"
	resp, err := http.Post(getApiUrl("/chat/"+role), contentType, bytes.NewBuffer([]byte(bytesData)));

	if err != nil {
		return "error"
	}
	defer resp.Body.Close()

	buf := new(bytes.Buffer)
	buf.ReadFrom(resp.Body)

	return buf.String()
}