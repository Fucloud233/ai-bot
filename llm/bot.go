package llm

import (
	"ai-bot/model"
	"bytes"
	"encoding/json"
	"fmt"
	"net/http"
)

func getApiUrl(path string) string {
	return "http://localhost:6061" + path
}

func postRequest(apiUrl string, body map[string]interface{}) string {
	bytesData, _ := json.Marshal(body)

	const contentType = "application/json"
	resp, err := http.Post(apiUrl, contentType, bytes.NewBuffer([]byte(bytesData)));

	if err != nil {
		return fmt.Sprint(err)
	}
	defer resp.Body.Close()

	buf := new(bytes.Buffer)
	buf.ReadFrom(resp.Body)

	return buf.String()
}


// the number of messages couldn't be odd
// so we should append answer about the assistant
func wrapBasicPrompt(basicPrompt string, answer string) []model.SimpleMessage {
	messages := []model.SimpleMessage {
		model.NewSimpleMessage(model.User, basicPrompt),
		model.NewSimpleMessage(model.Assistant, answer),
	}

	return messages
}

func ChatWithRoleOld(role string, roleDescription string, historyMessages []model.Message, userMessage string)  string {
	// 1. merge the basic prompt and role 
	basic_prompt := 	
		// (1) basic role prompt
		fmt.Sprintf("你现在是我的%s。", model.GetRoleName(role)) +
		// (2) description about role from user
		roleDescription + "\n" +
		// (3) some prompt about this project
		"我现在学习、工作或者生活上有点压力，请你帮我缓解一下我和压力和焦虑。"+
        "请控制你的回答在20个字之间。"

	fmt.Println("Prompt: ", basic_prompt)

	messages := wrapBasicPrompt(basic_prompt, "好的，我一定会控制回答字数的")

	// push the historyMessage into messageList
	for _, message := range historyMessages {
		messages = append(messages, message.ToSimpleMessage())
	}

	// append user message 
	messages = append(messages, model.NewSimpleMessage(model.User, userMessage))

	body := map[string]interface{}{
		"messages": messages,
	}

	apiUrl := getApiUrl("/chat")

	return postRequest(apiUrl, body)
}

// this operation won't merge the message list
// the merge task will be given to `python backend`
func ChatWithRole(role string, roleDescription string, historyMessages []model.Message, userMessage string)  string {
	apiUrl := getApiUrl("/chat")

	body := map[string]interface{}{
		"botRole": role,
		"botRoleDescription": roleDescription,
		"historyMessages": historyMessages,
		"userMessage": userMessage,
	}

	return postRequest(apiUrl, body)
}